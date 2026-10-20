import csv, os
from datetime import datetime
import numpy as np
from qiskit import QuantumCircuit
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

import urllib.request
topic_file = os.path.expanduser("~/.ntfy_topic")
TOPIC = open(topic_file).read().strip() if os.path.exists(topic_file) else None

def notify(msg):
    if not TOPIC:
        return
    try:
        urllib.request.urlopen(f"https://ntfy.sh/{TOPIC}", data=msg.encode(), timeout=10)
    except Exception as e:
        print("notify failed:", e)

backend = QiskitRuntimeService().backend("ibm_kingston")
status = backend.status()
if not status.operational or status.status_msg != "active":
    print(datetime.now().isoformat(timespec="minutes"), "skipped:", status.status_msg)
    notify(f"CHSH skipped: {status.status_msg}")
    raise SystemExit
LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "daily_results.csv")

# --- A: the game (same as chsh.py) ---
ALICE = {0: 0.0, 1: np.pi/2}
BOB   = {0: np.pi/4, 1: -np.pi/4}
PAIRS = [(x, y) for x in (0, 1) for y in (0, 1)]
LAYOUTS = {"(0,1)": [0, 1], "(109,118)": [109, 118]}

def chsh_circuit(x, y):
    qc = QuantumCircuit(2, 2)
    qc.h(0); qc.cx(0, 1)
    qc.ry(-ALICE[x], 0)
    qc.ry(-BOB[y], 1)
    qc.measure([0, 1], [0, 1])
    return qc

def win_rate(counts, x, y):
    wins = 0
    for bits, n in counts.items():
        b, a = int(bits[0]), int(bits[1])
        if (a ^ b) == (x & y): wins += n
    return wins / sum(counts.values())

# --- B: calibration score (same as best_pairs.py) ---
def calibration_score(q0, q1):
    cz, meas = backend.target["cz"], backend.target["measure"]
    errs = [cz[(q0, q1)].error, meas[(q0,)].error, meas[(q1,)].error]
    return sum(errs) if None not in errs else float("nan")

# --- C: run both pairs in one job ---
circuits, labels = [], []
for name, layout in LAYOUTS.items():
    pm = generate_preset_pass_manager(backend=backend, optimization_level=1,
                                      initial_layout=layout)
    for x, y in PAIRS:
        circuits.append(pm.run(chsh_circuit(x, y)))
        labels.append((name, x, y))

job = Sampler(mode=backend).run(circuits, shots=4000)
print("submitted", job.job_id(), flush=True)
result = job.result()
usage = job.usage()
now = datetime.now().isoformat(timespec="minutes")

# --- D: append one row per pair to the CSV ---
new_file = not os.path.exists(LOG)
with open(LOG, "a", newline="") as f:
    w = csv.writer(f)
    if new_file:
        w.writerow(["time", "job_id", "pair", "calib_score",
                    "r00", "r01", "r10", "r11", "avg", "usage_s"])
    summary = []
    for name, layout in LAYOUTS.items():
        r = [win_rate(result[i].data.c.get_counts(), x, y)
             for i, (n, x, y) in enumerate(labels) if n == name]
        w.writerow([now, job.job_id(), name,
                    round(calibration_score(*layout), 5),
                    *[round(v, 4) for v in r], round(np.mean(r), 4),
                    usage])
        summary.append(f"{name} {np.mean(r):.3f}")
print("logged", now, job.job_id())
notify(f"CHSH {now}: " + " | ".join(summary) + f" | {usage:.1f}s")

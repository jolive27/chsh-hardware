import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit import transpile
from qiskit_ibm_runtime import QiskitRuntimeService
backend = QiskitRuntimeService().backend("ibm_kingston")

ALICE = {0: 0.0, 1: np.pi/2}         # Alice's angle for question x
BOB   = {0: np.pi/4, 1: -np.pi/4}    # Bob's angle for question y

def chsh_circuit(x, y):
    qc = QuantumCircuit(2, 2)
    qc.h(0); qc.cx(0, 1)             # share an entangled pair
    qc.ry(-ALICE[x], 0)              # aim Alice's measurement
    qc.ry(-BOB[y], 1)                # aim Bob's measurement
    qc.measure([0, 1], [0, 1])
    return qc

def win_rate(counts, x, y):
    wins = 0
    for bits, n in counts.items():
        b, a = int(bits[0]), int(bits[1])   # Qiskit prints Bob's bit first
        if (a^b) == (x&y): wins += n
    return wins / sum(counts.values())

sim = AerSimulator.from_backend(backend)
rates = []
for x in (0, 1):
    for y in (0, 1):
        counts = sim.run(transpile(chsh_circuit(x, y), sim), shots=4000).result().get_counts()
        rates.append(win_rate(counts, x, y))
print("win rate:", np.mean(rates))   # classical limit 0.75, quantum about 0.854

from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime import SamplerV2 as Sampler

layouts = {"(0,1)": [0, 1], "(109,118)": [109, 118]}
pairs = [(x, y) for x in (0, 1) for y in (0, 1)]
circuits, labels = [], []
for name, layout in layouts.items():
    pm = generate_preset_pass_manager(backend=backend, optimization_level=1,
                                      initial_layout=layout)
    for x, y in pairs:
        circuits.append(pm.run(chsh_circuit(x, y)))
        labels.append((name, x, y))

job = Sampler(mode=backend).run(circuits, shots=4000)
print("Job ID:", job.job_id())
result = job.result()
for name in layouts:
    r = [win_rate(result[i].data.c.get_counts(), x, y)
         for i, (n, x, y) in enumerate(labels) if n == name]
    print(name, [round(v, 3) for v in r], "average:", round(sum(r)/len(r), 3))

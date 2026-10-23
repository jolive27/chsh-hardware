import json, os
from qiskit_ibm_runtime import QiskitRuntimeService
from datetime import datetime

service = QiskitRuntimeService()
backend = service.backend("ibm_kingston")
os.makedirs("data/raw", exist_ok=True)          # make the folder if it's missing

for job in service.jobs(backend_name="ibm_kingston", limit=100):
    path = f"data/raw/{job.job_id()}.json"
    if os.path.exists(path):                     # already saved: skip
        continue
    if job.status() != "DONE":                   # still queued or failed: skip
        continue
    result = job.result()
    ran_at = job.metrics()["timestamps"]["running"]
    layouts = [pub[0].layout.final_index_layout() for pub in job.inputs["pubs"]]
    props = backend.properties(datetime=datetime.fromisoformat(ran_at))
    cal = {}
    for q in sorted({q for lay in layouts for q in lay}):  # Every physical qubit used
        vals = {n.name: n.value for n in props.qubits[q]}
        dates = {n.name: n.date for n in props.qubits[q]}
        cal[q] = {"p01": vals["prob_meas1_prep0"],
                  "p10": vals["prob_meas0_prep1"],
                  "cal_time": dates["readout_error"].isoformat()}  # Really oughta initialize some of these as functions/variables, ugly
    try:
        counts = [pub.data.c.get_counts() for pub in result]
    except AttributeError:                       # an older job built differently
        print("skipped", job.job_id())
        continue
    with open(path, "w") as f:
        json.dump({"job_id": job.job_id(), "ran_at": ran_at, "layouts": layouts, "counts": counts, "cal": cal}, f, indent=1)
    print("saved", job.job_id(), len(counts), "circuits")

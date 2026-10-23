# Measuring lean of qubits by calculating how often each qubit in a pair reads 1 (healthy qubit reads 1 about half the time (0.500))
# How to run: python lean.py [job_id]; when no ID is given, runs most recent job
import sys
from qiskit_ibm_runtime import QiskitRuntimeService
service = QiskitRuntimeService()

job_id = sys.argv[1] if len(sys.argv) > 1 else service.jobs(limit=1, backend_name="ibm_kingston")[0].job_id()
job = service.job(job_id)
result = job.result()
settings = ["(0,0)", "(0,1)", "(1,0)", "(1,1)"]
print("pair        x,y  alice  bob") # Header line for outputs
for i, pub in enumerate(result):
    pair = "(0,1)" if i < 4 else "(109,118)"
    setting = settings[i % 4]
    counts = pub.data.c.get_counts()
    shots = sum(counts.values())
    alice_ones = 0
    bob_ones = 0
    for s, n in counts.items():
        if s[1] == "1": # Qiskit bitstrings put Bob's bit first: s[0] = Bob, s[1] = Alice
            alice_ones += n
        if s[0] == "1":
            bob_ones += n
    print(f"{pair:10} {setting} {alice_ones/shots:.3f} {bob_ones/shots:.3f}") # Rounds outputs to 3 decimal places
print(job.usage(), "seconds")

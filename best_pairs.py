from qiskit_ibm_runtime import QiskitRuntimeService
backend = QiskitRuntimeService().backend("ibm_kingston")

cz, meas = backend.target["cz"], backend.target["measure"]

def score(pair):
    errs = [cz[pair].error, meas[(pair[0],)].error, meas[(pair[1],)].error]
    return sum(errs) if None not in errs else 1.0

best = sorted(cz.keys(), key=score)[:5]
for p in best:
    print(p, round(score(p), 4))

print("pair (0, 1):", round(score((0, 1)), 4))

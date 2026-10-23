# Checks IBM's own qubit readout and calibration data and prints them out
from qiskit_ibm_runtime import QiskitRuntimeService
service = QiskitRuntimeService()
props = service.backend("ibm_kingston").properties()
for q in (0, 1, 109, 118):
    values = {n.name: round(n.value, 4) for n in props.qubits[q]}
    for n in props.qubits[q]:
        if n.name == "readout_error":
            readout_date = n.date
    print(q, readout_date, values)

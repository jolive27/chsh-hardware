# Start here if you are new to python/qiskit (all code for setup will be directly in terminal or powershell).

This runs on my raspberry pi every night at 3am after only a week of learning. If you want to run it yourself once, follow instructions. Will take ~10 minutes

---

Install Python (3.11 or newer) from python.org. Open terminal (MacOS) or powershell (Windows) (or ask AI) and run

```
python --version
```

to make sure it downloaded

---

After downloading python, run

```
pip install qiskit qiskit-aer qiskit-ibm-runtime
```

This installs all necessary packages

---

Make a free account at quantum.cloud.ibm.com. You get 10 free minutes a month on real quantum computers; one run of chsh.py takes about 11 seconds of it.

---

Grab your API key and instance CRN off the dashboard and save them once by running:

```
python -c "from qiskit_ibm_runtime import QiskitRuntimeService; QiskitRuntimeService.save_account(token='PASTE_YOUR_API_KEY', instance='YOUR_CRN')"
```

No CRN on the page? `instance='ibm-q/open/main'` works too. This is the last annoying step.

---

Download this repo (green Code button, Download ZIP), unzip it, open a terminal/powershell in the folder. (Right click folder and click new terminal at folder)

---

```
python chsh.py
```

— simulated results run first and prints a win rate around 0.8, then it submits to the actual quantum computer (ibm_kingston) and sits in a queue for a bit (depends on traffic). End result should be pair 109-118 around 0.84 and pair 0-1 somewhere 0.55-0.70.

---

```
python best_pairs.py
```

— ranks qubit pairs by IBM's own error numbers. Doesn't use any minutes.


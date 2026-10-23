# CHSH Bell test on IBM quantum hardware

I run the CHSH game every night on IBM's `ibm_kingston`, on two qubit pairs.
Pair 109-118 beats the classical limit every run. Pair 0-1 never does, and the
per-run data points to a bias on qubit 0 that IBM's calibration never reported.

## The game
| Strategy | Best possible win rate |
|---|---|
| Classical | 0.75 |
| Quantum (entangled qubits) | cos²(π/8) ≈ 0.854 |

Alice and Bob get random bits x and y and answer a and b. They win if
a XOR b = x AND y. Each run plays all four (x, y) settings, 4,000 shots each.

## Results at a glance
| Pair | Runs | Mean win rate | Range of run averages | Beats 0.75? |
|---|---|---|---|---|
| 109-118 | 5 | 0.838 | 0.834–0.840 | Every run |
| 0-1 | 6 | 0.627 | 0.556–0.692 | Never |

## Run by run
| Run (ET) | Win, 0-1 | Win, 109-118 | Qubit 0 reads 1 | Qubit 1 reads 1 | IBM: q0 misreads 0 as 1 | IBM: q1 misreads 0 as 1 |
|---|---|---|---|---|---|---|
| *Healthy* | *~0.85* | *~0.85* | *0.50* | *0.50* | *~1%* | *~1%* |
| Oct 19, 11:31 PM | 0.631 | | **0.68** | 0.58 | 0.3% | 0.6% |
| Oct 19, 11:39 PM | 0.637 | 0.840 | **0.65** | 0.58 | 0.3% | 0.6% |
| Oct 20, 10:34 PM | 0.692 | 0.837 | **0.59** | 0.56 | 1.2% | 0.7% |
| Oct 21, 3:00 AM | 0.670 | 0.840 | **0.61** | 0.56 | 0.05% | **70%** |
| Oct 22, 3:00 AM | 0.574 | 0.840 | **0.82** | 0.47 | 0.6% | 0.1% |
| Oct 23, 3:00 AM | 0.556 | 0.834 | **0.84** | 0.48 | 1.0% | 0.3% |

- Qubit 0 reads 1 too often in every run, and pair 0-1's win rate drops as the bias grows.
- IBM's calibration (the one in effect at each run) reported qubit 0 as near-perfect every time.
- Pair 109-118's qubits read 1 between 0.47 and 0.51 in every run.

## How the finding evolved
| Date | Hypothesis | Evidence | Status |
|---|---|---|---|
| Oct 19 | Pair 0-1 underperforms its calibration | ~0.63 on hardware vs ~0.82 in a noisy simulation | Confirmed |
| Oct 21 | Qubit 1's readout is the cause | Live calibration showed qubit 1 misreading 69% of 0s; predicted ~0.56, Oct 22 measured 0.574 | Rejected: the calibration in effect before the Oct 22 run had qubit 1 healthy, so the match was timing |
| Oct 23 | Qubit 0 is biased toward reading 1 | Qubit 0 reads 1 59–84% of the time in every run; win rate tracks it | Current |

## Open questions
- Is qubit 0's bias in readout, or in the state before measurement? Next step: readout-test circuits in every run.
- A rough readout-only estimate leaves about 0.05 of the drop unexplained. Two-qubit gate error?
- How fast does the bias drift? IBM's roughly daily calibrations can't resolve it.

## How it runs
| When | Script | What it does |
|---|---|---|
| 3:00 AM | `daily_chsh.py` | Runs both pairs in one job, sends a push notification |
| 4:00 AM | `collect.py` | Saves counts, run time, physical qubits and run-time calibration to `data/raw/` |
| 4:00 AM | `build_table.py` | Rebuilds `data/runs.csv` from the raw files |
| Anytime | `lean.py`, `calib.py` | Lean of one job; IBM's current calibration |

Data: [`data/runs.csv`](data/runs.csv), one row per job per circuit.

Setup: Python, `qiskit`, `qiskit-ibm-runtime`, and a free IBM Quantum account with 10 free minutes a month (average 11s per job).

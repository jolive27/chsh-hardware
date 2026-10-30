# CHSH Bell test on IBM quantum hardware (Updated as of Oct. 30, 2026)

I run the CHSH game from my raspberry pi every night using cron on IBM's `ibm_kingston`, on two qubit pairs with help from IBM's own documentation.

The two pairs chosen (0, 1) and (109, 118) turned to be a fun experiment: 109-118 stayed healthy the whole time (picked from IBM's own calibration data at the start), 0-1 was "broken" for a week in a way that could be diagnosed from my own run data. It then recovered after October 28.

## The game
| Strategy | Best possible win rate |
|---|---|
| Classical | 0.75 |
| Quantum (entangled qubits) | cos²(π/8) ≈ 0.854 |

Alice and Bob (the two qubits in a pair, classically named Alice and Bob for whatever reason) get random bits x and y and answer a and b. They win if a XOR b = x AND y. Each run plays all four (x, y) settings, 4,000 shots each.


## Headline results

| Pair | Period | Runs | Mean win rate | Range |
|---|---|---|---|---|
| (109, 118) | Oct 20–30, 2026 | 11 | 0.840 | 0.834–0.845 |
| (0, 1) | Oct 20–27 ("broken") | 10 | 0.604 | 0.548–0.692 |
| (0, 1) | Oct 29–30 (post-recalibration) | 2 | 0.838 | 0.833–0.842 |

Pair (109, 118) beat the classical bound on every run. Pair (0, 1) never did
during its "broken" period. Then, after IBM recalibrated the device, posted
0.833 and 0.842, statistically indistinguishable from the control pair.

## Rough data visualization (tried to do it using matplotlib but could not get it to look right)

Nightly mean win rates — `o` = pair (0, 1), `#` = pair (109, 118),
`*` = both pairs in the same cell. The quantum ideal, 0.854, sits just
above the 0.84 band.

    Oct   20  21  22  23  24  25  26  27  28  29  30
    0.90 |
    0.88 |
    0.86 |
    0.84 | #   #   #   #   #   #   #   #       *   *
    0.82 |
    0.80 |
    0.78 |
    0.76 |
    0.75 |- - - - - - - - - - - - - - - - - - - - - - -  classical bound
    0.74 |
    0.72 |
    0.70 |
    0.68 |     o
    0.66 |
    0.64 | o
    0.62 |
    0.60 |
    0.58 |         o       o       o
    0.56 |             o       o
    0.54 |                             o

| Night (Oct 2026) | Pair (0, 1) | Pair (109, 118) |
|---|---|---|
| 20 | 0.634 | 0.840 |
| 21 | 0.681 | 0.839 |
| 22 | 0.574 | 0.840 |
| 23 | 0.556 | 0.834 |
| 24 | 0.571 | 0.843 |
| 25 | 0.568 | 0.840 |
| 26 | 0.588 | 0.845 |
| 27 | 0.548 | 0.834 |
| 28 | no run (internet out) | no run |
| 29 | 0.833 | 0.840 |
| 30 | 0.842 | 0.840 |

(Oct 20–21 nights average two jobs for pair 0-1;
all other nights are single jobs of 16,000 shots per pair.)

## What the data establishes — and what it doesn't

Established:

- The fault is mostly on qubit 0. Its measured ones-rate rose from ≈ 0.67
  on Oct 20 to 0.88 by Oct 27 while the win rate fell in step. On the
  post-recalibration runs the "ones-rate" is 0.49 and the win rate is back at
  ≈ 0.84.
- IBM's own runtime calibrations never described it: they reported qubit 0's
  readout errors as small (≈ 1%) and near-symmetric all week, which predicts
  a win rate of ≈ 0.84 every night (except Oct.21). Qubit 0's counts imply an
  effective 0→1 asymmetry of roughly 0.76 at its worst.
- The control pair rules out device-wide erros (same nights and same backend).

Not yet identified:

- The fridge-level physical cause is inside IBM and not knowable from
  outside.
- If the fault ever recurs, three circuits settle the stage in one session:
  prepare |0⟩ and measure, prepare |1⟩ and measure (the true flip rates,
  model-free), and a no-entanglement single-qubit marginal probe.


## My Verdict

 - The true error of qubit 0 in ibm_kingston can be measured, but the mechanism
   and the physical cause of the error are unestablished in this experiment.

## How it runs

A Raspberry Pi submits the job at 03:00, collects results at 04:00, and syncs
this repo at 04:05 (US Eastern). See `AUTOMATED_PIPELINE.md` and `crontab.txt`.

- `daily_chsh.py` — builds and submits the 8 circuits, logs a summary row
- `collect.py` — sweeps finished jobs, saves raw counts + calibration snapshots to `data/raw/`
- `build_table.py` — rebuilds `data/runs.csv` from the raw files
- `data/runs.csv` — the canonical dataset (one row per circuit)
- `daily_results.csv` — early summary log, superseded by `data/runs.csv`; kept for history

Setup: Python, `qiskit`, `qiskit-ibm-runtime`, and a free IBM Quantum account with 10 free minutes a month (average 11s per job).

## Other notes

- **Oct 28, 2026 is missing.** The Pi's internet connection failed overnight
  (Spectrum scheduled maintenance) and the 3 AM submission never happened.
- The Oct 29 job waited ~9 hours in IBM's queue and ran at 11:57 AM; the
  submission script died during the wait, but the 04:00 collector recovered
  the finished job the following night. No data lost.
- I have not yet taken a formal quantum mechanics course, so I did most of the
  learning for this using Mary Boas's "Mathematical Methods in the Physical Sciences"
  and Griffiths "Introduction to Quantum Mechanics".
- AKA, this is not an expert-level experiment and was more for my own educational value.

## License

MIT — see `LICENSE`.

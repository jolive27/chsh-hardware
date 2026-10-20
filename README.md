# CHSH on real IBM quantum hardware

Experimenting with real IBM quantum hardware by testing quantum vs. classical CHSH win rates.

## Finding

On Oct 19, 2026, the default layout placed the circuit on qubits (0, 1),
which lost to the classical limit despite modest published error rates.
Running on the best-calibrated pair, (109, 118), gave a near-ideal quantum result.

| Pair | Calibration error* | Win rate | CHSH S |
|---|---|---|---|
| (0, 1), default | 0.017 | 0.637 | 1.10 |
| (109, 118), best | 0.0095 | 0.840 | 2.72 |
| Ideal quantum | – | 0.854 | 2.83 |
| Classical limit | – | 0.750 | 2.00 |

Both pairs ran in the same job, 16,000 rounds each. A noisy simulation built
from the chip's calibration predicted about 0.82 for (0, 1).

*Two-qubit gate error plus both readout errors, from IBM's calibration data.

## Files
- `chsh.py`: the CHSH game in simulation, noisy simulation, and on hardware
- `best_pairs.py`: ranks qubit pairs by calibration error

## Job IDs
- `dbbe129gv2cc73e88l2g`: first hardware run, on (0, 1)
- `dbbe4v9gv2cc73e88trg`: both pairs in one job

## Next steps
- Per-round win rates, and a readout test on (0, 1)
- Repeat on other days to see whether (0, 1) stays bad
- Map the chip: how often does calibration data mislead?

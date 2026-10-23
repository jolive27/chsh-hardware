import csv, glob, json

SETTINGS = [(0,0), (0,1), (1,0), (1,1)]
rows = []
for path in glob.glob("data/raw/*.json"):
    d = json.load(open(path))
    for i, counts in enumerate(d["counts"]):
        a, b = d["layouts"][i]  # physical qubits: Alice, Bob
        x, y = SETTINGS[i % 4]
        shots = sum(counts.values())
        wins = a_ones = b_ones = 0
        for s, n in counts.items():
            alice, bob = int(s[1]), int(s[0])  #s[1] = Alice, s[0] = Bob
            if (alice ^ bob) == (x & y):
                wins += n
            if alice == 1:
                a_ones += n
            if bob == 1:
                b_ones += n

        cal_a, cal_b = d["cal"][str(a)], d["cal"][str(b)]
        rows.append({"job_id": d["job_id"], "ran_at": d["ran_at"],
                     "pair": f"{a}-{b}", "x": x, "y": y, "shots":shots,
                     "win": round(wins / shots, 4),
                     "a_ones": round(a_ones / shots, 4),
                     "b_ones": round(b_ones / shots, 4),
                     "a_p01": round(cal_a["p01"], 4), "a_p10": round(cal_a["p10"], 4),
                     "b_p01": round(cal_b["p01"], 4), "b_p10": round(cal_b["p10"], 4),
                     "cal_time": cal_a["cal_time"]})  # Ugliest code I've ever written... but it works
rows.sort(key=lambda r: r["ran_at"])
with open("data/runs.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)

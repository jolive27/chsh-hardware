# Nightly data collection pipeline

Runs on my Raspberry Pi (cron). All times US Eastern.

- **03:00** — `daily_chsh.py` — runs both qubit pairs on ibm_kingston computer,
  appends to `daily_results.csv`, sends push notification through NTFY app. Log: `daily.log`
- **04:00** — `collect.py` then `build_table.py` — fetches each job's data
  plus the calibration in effect at run time into `data/raw/`, rebuilds
  `data/runs.csv`. Log: `collect.log`
- **04:05** — github data sync — `git add -A && git commit && git pull --rebase
  && git push`. Log: `git.log`

Exact crontab job is saved in `crontab.txt`

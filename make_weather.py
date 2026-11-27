import csv
from datetime import date, timedelta

start = date(2026, 9, 1)
with open("data/weather.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["date", "t_min", "t_max"])
    for i in range(120):
        t_min = 14 + (i % 7) * 0.5  # It varies a little from day to day
        writer.writerow([start + timedelta(days=i), t_min, t_min + 11])
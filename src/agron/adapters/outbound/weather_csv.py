"""Adapter de clima: implementa o port WeatherProvider lendo um CSV com Polars."""
from datetime import date
from pathlib import Path

import polars as pl


class CsvWeatherProvider:
    def __init__(self, path: Path) -> None:
        self.path = path

    def daily_weather(self, start: date, end: date) -> pl.DataFrame:
        return (
            pl.scan_csv(self.path, try_parse_dates=True)
            .filter(pl.col("date").is_between(start, end))
            .select("date", "t_min", "t_max")
            .collect()
        )
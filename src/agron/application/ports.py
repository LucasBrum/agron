"""Ports: o que a aplicação precisa do mundo de fora, sem saber como é feito."""
from datetime import date
from typing import Protocol
from uuid import UUID

import polars as pl

from agron.domain.models import Field


class FieldRepository(Protocol):
    def save(self, field: Field) -> Field: ...

    def get(self, field_id: UUID) -> Field | None: ...


class WeatherProvider(Protocol):
    def daily_weather(self, start: date, end: date) -> pl.DataFrame:
        """Retorna as colunas: date, t_min, t_max."""
        ...
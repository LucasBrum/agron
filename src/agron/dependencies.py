"""Composição: liga cada port ao adapter real. Nos testes, trocamos estas funções."""
from pathlib import Path
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from agron.adapters.outbound.db import SqlAlchemyFieldRepository, get_session
from agron.adapters.outbound.weather_csv import CsvWeatherProvider
from agron.application.ports import FieldRepository, WeatherProvider

WEATHER_CSV = Path("data/weather.csv")


def get_field_repository(session: Annotated[Session, Depends(get_session)]) -> FieldRepository:
    return SqlAlchemyFieldRepository(session)


def get_weather_provider() -> WeatherProvider:
    return CsvWeatherProvider(WEATHER_CSV)
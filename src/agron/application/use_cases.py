from dataclasses import dataclass
from datetime import date
from uuid import UUID

from agron.application.ports import FieldRepository, WeatherProvider
from agron.domain.agronomy import crop_stage, growing_degree_days
from agron.domain.models import Field


class FieldNotFound(Exception):
    pass


@dataclass
class Recommendation:
    field_id: UUID
    as_of: date
    growing_degree_days: float
    stage: str


class CreateField:
    def __init__(self, repo: FieldRepository) -> None:
        self.repo = repo

    def execute(self, field: Field) -> Field:
        return self.repo.save(field)


class GetField:
    def __init__(self, repo: FieldRepository) -> None:
        self.repo = repo

    def execute(self, field_id: UUID) -> Field:
        field = self.repo.get(field_id)
        if field is None:
            raise FieldNotFound(field_id)
        return field


class RecommendForField:
    def __init__(self, repo: FieldRepository, weather: WeatherProvider) -> None:
        self.repo = repo
        self.weather = weather

    def execute(self, field_id: UUID, as_of: date) -> Recommendation:
        field = GetField(self.repo).execute(field_id)
        df = self.weather.daily_weather(field.planting_date, as_of)
        gdd = growing_degree_days(df)
        return Recommendation(field_id, as_of, round(gdd, 1), crop_stage(gdd))
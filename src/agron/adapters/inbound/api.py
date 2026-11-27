"""Adapter de entrada: rotas HTTP. Só traduz HTTP <-> casos de uso."""
from datetime import date
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field as PydField

from agron.application.ports import FieldRepository, WeatherProvider
from agron.application.use_cases import (
    CreateField,
    FieldNotFound,
    GetField,
    RecommendForField,
)
from agron.dependencies import get_field_repository, get_weather_provider
from agron.domain.models import Field

router = APIRouter(prefix="/fields", tags=["fields"])

Repo = Annotated[FieldRepository, Depends(get_field_repository)]
Weather = Annotated[WeatherProvider, Depends(get_weather_provider)]


class FieldIn(BaseModel):
    name: str = PydField(min_length=1, max_length=100)
    crop: str = PydField(min_length=1, max_length=50)
    area_ha: float = PydField(gt=0)
    planting_date: date


class FieldOut(FieldIn):
    id: UUID


class RecommendationOut(BaseModel):
    field_id: UUID
    as_of: date
    growing_degree_days: float
    stage: str


def to_out(field: Field) -> FieldOut:
    return FieldOut(
        id=field.id,
        name=field.name,
        crop=field.crop,
        area_ha=field.area_ha,
        planting_date=field.planting_date,
    )


@router.post("", status_code=status.HTTP_201_CREATED)
def create_field(body: FieldIn, repo: Repo) -> FieldOut:
    field = Field(body.name, body.crop, body.area_ha, body.planting_date)
    return to_out(CreateField(repo).execute(field))


@router.get("/{field_id}")
def get_field(field_id: UUID, repo: Repo) -> FieldOut:
    try:
        return to_out(GetField(repo).execute(field_id))
    except FieldNotFound:
        raise HTTPException(status_code=404, detail="Field not found")


@router.get("/{field_id}/recommendation")
def recommendation(field_id: UUID, as_of: date, repo: Repo, weather: Weather) -> RecommendationOut:
    try:
        rec = RecommendForField(repo, weather).execute(field_id, as_of)
    except FieldNotFound:
        raise HTTPException(status_code=404, detail="Field not found")
    return RecommendationOut(**rec.__dict__)
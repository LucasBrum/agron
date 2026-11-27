from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

@dataclass
class Field:
    """ A field: an area of a farm where a crop was planted """

    name: str
    crop: str
    area_ha: float
    planting_date: date
    id: UUID | None = None

    def __post_init__(self) -> None:
        if self.area_ha <= 0:
            raise ValueError("area_ha must be greater than zero")
        if self.id is None:
            self.id = uuid4()

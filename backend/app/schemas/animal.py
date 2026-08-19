from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.animal import CoatType, Size, Species


class AnimalCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=100)
    species: Species
    breed: str | None = Field(default=None, max_length=100)
    size: Size | None = Field(default=None)
    coat_type: CoatType | None = Field(default=None)
    age: int | None = Field(default=None, ge=0, le=40)
    notes: str | None = None


class AnimalUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str | None = Field(default=None, min_length=1, max_length=100)
    species: Species | None = Field(default=None)
    breed: str | None = Field(default=None, max_length=100)
    size: Size | None = Field(default=None)
    coat_type: CoatType | None = Field(default=None)
    age: int | None = Field(default=None, ge=0, le=40)
    notes: str | None = None


class AnimalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    client_id: int
    name: str
    species: Species
    breed: str | None
    size: Size | None
    coat_type: CoatType | None
    age: int | None
    notes: str | None
    created_at: datetime
    updated_at: datetime


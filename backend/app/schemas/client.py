from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ClientCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    phone: str = Field(min_length=1, max_length=30)
    email: str | None = Field(default=None, max_length=255)
    notes: str | None = None


class ClientUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    first_name: str | None = Field(default=None, min_length=1, max_length=100)
    last_name: str | None = Field(default=None, min_length=1, max_length=100)
    phone: str | None = Field(default=None, min_length=1, max_length=30)
    email: str | None = Field(default=None, max_length=255)
    notes: str | None = None


class ClientResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str
    phone: str
    email: str | None
    notes: str | None
    created_at: datetime
    updated_at: datetime
# Pydantic
from pydantic import BaseModel, Field

# Python
from datetime import datetime


class EventSchema(BaseModel):
    """Schema for serialize just one event."""

    id: int = Field(ge=0)
    title: str = Field(max_length=200)
    date: datetime = Field()
    is_finished: bool = Field()
    telegram_id: int = Field(ge=0)


class EventsSchema(BaseModel):
    """Schema for serialize all events."""

    response: list[EventSchema]


class CreateEventSchema(BaseModel):
    """Schema for create an Event."""

    title: str = Field(max_length=200)
    date: datetime = Field()
    telegram_id: int = Field(ge=0)


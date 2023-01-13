from __future__ import annotations

from pydantic import BaseModel


class Faction(BaseModel):
    key: str
    ordinal: int
    label: str


class Factions(BaseModel):
    __root__: list[Faction]

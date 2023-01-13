from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

from src.model.artifact_bonus import ArtifactBonus


class ArtifactSet(BaseModel):
    key: str
    ordinal: int
    label: str
    set_size: int = Field(..., alias='setSize')
    bonuses: Optional[list[ArtifactBonus]] = []
    description: str


class ArtifactSets(BaseModel):
    __root__: list[ArtifactSet]

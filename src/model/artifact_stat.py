from __future__ import annotations

from pydantic import BaseModel


class ArtifactStat(BaseModel):
    key: str
    ordinal: int
    label: str
    enhanceable: bool


class ArtifactStats(BaseModel):
    __root__: list[ArtifactStat]

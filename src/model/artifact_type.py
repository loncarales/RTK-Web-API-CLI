from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class ArtifactType(BaseModel):
    key: str
    ordinal: int
    label: str
    plural: str
    is_accessory: bool = Field(..., alias='isAccessory')
    min_rank: Optional[int] = Field(None, alias='minRank')
    ascension_level: Optional[int] = Field(None, alias='ascensionLevel')


class ArtifactTypes(BaseModel):
    __root__: list[ArtifactType]

from pydantic import BaseModel, Field


class ArtifactBonus(BaseModel):
    kind: str
    absolute: bool
    value: float
    glyph_power: float = Field(None, alias="glyphPower")
    level: int | None

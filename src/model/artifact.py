from __future__ import annotations

from pydantic import BaseModel, Field

from src.model.artifact_bonus import ArtifactBonus


class Artifact(BaseModel):
    id: int
    sell_price: int = Field(..., alias='sellPrice')
    price: int
    level: int
    activated: bool
    kind_id: str = Field(..., alias='kindId')
    rank: str
    rarity: str
    set_kind_id: str = Field(..., alias='setKindId')
    seen: bool
    failed_upgrades: int = Field(..., alias='failedUpgrades')
    primary_bonus: ArtifactBonus = Field(..., alias='primaryBonus')
    secondary_bonuses: list[ArtifactBonus] = Field(..., alias='secondaryBonuses')
    faction: str
    all_stats: dict[str, float] = Field(..., alias='allStats')


class Artifacts(BaseModel):
    __root__: list[Artifact]


class ArtifactDto(BaseModel):
    id: int
    set: str
    type: str
    level: int
    rank: str
    rarity: str
    primary_stat: str
    substats: dict[str, str]


class ArtifactsDto(BaseModel):
    __root__: list[ArtifactDto]


def convert_to_artifact_dto(artifact: Artifact) -> ArtifactDto:
    return ArtifactDto(
        id=artifact.id,
        set=artifact.set_kind_id,
        type=artifact.kind_id,
        level=artifact.level,
        rank=convert_to_rank(artifact.rank),
        rarity=artifact.rarity,
        primary_stat=convert_to_primary_stat(artifact.primary_bonus),
        substats=convert_to_substats(artifact.secondary_bonuses)
    )


def convert_to_artifacts_dto(artifact_list: Artifacts) -> ArtifactsDto:
    return ArtifactsDto(__root__=[convert_to_artifact_dto(a) for a in artifact_list.__root__])


def convert_to_rank(rank: str) -> str:
    rank_mapping = {
        "One": "*",
        "Two": "**",
        "Three": "***",
        "Four": "****",
        "Five": "*****",
        "Six": "******"
    }
    return rank_mapping.get(rank, "")


def convert_to_primary_stat(primary_bonus: ArtifactBonus) -> str:
    primary_stat_value = f'{primary_bonus.kind} {primary_bonus.value:.0f}'
    if not primary_bonus.absolute:
        primary_stat_value = f'{primary_bonus.kind} {primary_bonus.value * 100:.0f}%'
    return primary_stat_value


def convert_to_substats(secondary_bonuses: list[ArtifactBonus]) -> dict:
    substats = {}

    for bonus in secondary_bonuses:
        bonus_kind = bonus.kind
        if bonus.level > 0:
            bonus_kind = f'{bonus.kind}({bonus.level})'
        substat = round(bonus.value)
        if not bonus.absolute:
            substat = f'{bonus.value * 100:.0f}%'
        if bonus.glyph_power != 0:
            substat = f'{bonus.value:.0f}+{bonus.glyph_power:.0f}'
            if not bonus.absolute:
                substat = f'{bonus.value * 100:.0f}%+{bonus.glyph_power * 100:.0f}%'
        substats[bonus_kind] = substat
    return substats

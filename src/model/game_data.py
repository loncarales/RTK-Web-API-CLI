from pydantic import BaseModel

from src.model.artifact_set import ArtifactSet
from src.model.artifact_stat import ArtifactStat
from src.model.artifact_type import ArtifactType
from src.model.faction import Faction


class GameData(BaseModel):
    artifactTypes: dict[str, ArtifactType]
    artifactSets: dict[str, ArtifactSet]
    artifactStats: dict[str, ArtifactStat]
    factions: dict[str, Faction]

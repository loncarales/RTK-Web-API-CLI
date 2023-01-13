import json
from pathlib import Path

from src.model.artifact_set import ArtifactSet
from src.model.artifact_stat import ArtifactStat
from src.model.artifact_type import ArtifactType
from src.model.faction import Faction
from src.model.game_data import GameData


def get_project_root() -> Path:
    return Path(__file__).parent.parent


def load_game_data() -> GameData:
    root = get_project_root()
    # Load Artifact Types
    with open(f'{root}/game-data/artifact-types.json') as artifact_types_json:
        data = json.load(artifact_types_json)
        artifact_types = {d['key']: ArtifactType.parse_obj(d) for d in data}
    # Load Artifact Sets
    with open(f'{root}/game-data/artifact-sets.json') as artifact_sets_json:
        data = json.load(artifact_sets_json)
        artifact_sets = {d['key']: ArtifactSet.parse_obj(d) for d in data}
    # Load Artifact Sets
    with open(f'{root}/game-data/artifact-stats.json') as artifact_stats_json:
        data = json.load(artifact_stats_json)
        artifact_stats = {d['key']: ArtifactStat.parse_obj(d) for d in data}
    # Load Factions
    with open(f'{root}/game-data/factions.json') as factions_json:
        data = json.load(factions_json)
        factions = {d['key']: Faction.parse_obj(d) for d in data}

    game_data = GameData(
        artifactTypes=artifact_types,
        artifactSets=artifact_sets,
        artifactStats=artifact_stats,
        factions=factions
    )
    return game_data


async def read_json_data(file_path: str, file_name: str, json_key: str):
    root = get_project_root()
    with open(f'{root}/{file_path}/{file_name}') as raid_json_file:
        parsed_json = json.load(raid_json_file)
        if json_key != "":
            parsed_json = parsed_json[json_key]
        return parsed_json

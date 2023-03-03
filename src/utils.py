import json
from pathlib import Path


def get_project_root() -> Path:
    return Path(__file__).parent.parent


def ln10():
    root = get_project_root()
    # Load l10n-en
    with open(f"{root}/game-data/l10n-en.json") as locale_json:
        return json.load(locale_json)


def skills():
    root = get_project_root()
    # Load skills-index
    with open(f"{root}/game-data/skills-index.json") as skills_json:
        return json.load(skills_json)


def load_static_data():
    root = get_project_root()
    # Load l10n-en
    l10n = ln10()
    # Load Artifact Sets
    with open(
        f"{root}/game-data/artifact-sets-index.json"
    ) as artifact_sets_json:
        data = json.load(artifact_sets_json)
        for kind in data["setKinds"].values():
            name = l10n[kind["name"]["key"]]
            kind["name"] = name
            short_description = l10n[kind["shortDescription"]["key"]]
            kind["shortDescription"] = short_description
            long_description = l10n[kind["longDescription"]["key"]]
            kind["longDescription"] = long_description
    static_data = {"l10n": ln10(), "artifact_sets": data["setKinds"]}
    return static_data


async def read_json_data(file_path: str, file_name: str, json_key: str):
    root = get_project_root()
    with open(f"{root}/{file_path}/{file_name}") as raid_json_file:
        parsed_json = json.load(raid_json_file)
        if json_key != "":
            parsed_json = parsed_json[json_key]
        return parsed_json

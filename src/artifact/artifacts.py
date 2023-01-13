import asyncio

import click
from rich import print
from rich.console import Console
from tabulate import tabulate

from src.model.artifact import Artifacts, convert_to_artifacts_dto
from src.service.rtk_web_api import RTKWebApi
from src.utils import load_game_data


@click.group()
def artifacts() -> None:
    """
    Manages artifacts resources
    """
    pass


@artifacts.command()
@click.pass_context
@click.option(
    "--level",
    "-l",
    required=False,
    multiple=True,
    type=int,
    help="Filter by the artifact level",
)
@click.option(
    "--rank",
    "-r",
    required=False,
    multiple=True,
    type=int,
    help="Filter by the artifact rank",
)
@click.option(
    "--rarity",
    "-ra",
    required=False,
    multiple=True,
    type=str,
    help="Filter by the artifact rarity",
)
@click.option(
    "--artifact-set",
    "-as",
    required=False,
    multiple=True,
    type=str,
    help="Filter by the artifact set",
)
@click.option(
    "--artifact-type",
    "-at",
    required=False,
    multiple=True,
    type=str,
    help="Filter by the artifact type",
)
@click.option(
    "--primary-stat",
    "-ps",
    required=False,
    multiple=True,
    type=str,
    help="Filter by the artifact primary stat",
)
@click.option(
    "--substat",
    "-su",
    required=False,
    multiple=True,
    type=str,
    help="Filter by the artifact substat",
)
@click.option(
    "--sort",
    "-s",
    required=False,
    multiple=True,
    type=str,
    help="Sort artifacts by any stat",
)
def get_all(ctx, level, rank, rarity, artifact_set, artifact_type, primary_stat, substat, sort) -> None:
    """
    Get all Artifacts based on input options
    """
    asyncio.run(async_get_all(ctx, level, rank, rarity, artifact_set, artifact_type, primary_stat, substat, sort))


async def async_get_all(ctx, level, rank, rarity, artifact_set, artifact_type, primary_stat, substat, sort):
    with RTKWebApi(ctx.obj["MOCK_WEBSOCKET_API"]) as web_api:
        all_accounts = await web_api.client.AccountApi.get_accounts()
        all_artifacts = await web_api.client.AccountApi.get_artifacts(all_accounts[0]["id"])
        game_data = load_game_data()
        artifact_sets = game_data.artifactSets
        artifact_types = game_data.artifactTypes
        factions = game_data.factions
        artifact_stats = game_data.artifactStats
        # Iterate through the objects in the JSON file
        searched_artifacts = list()
        for data in all_artifacts:
            # Replace the setKind value
            data["setKindId"] = artifact_sets.get(data["setKindId"]).label if data["setKindId"] in artifact_sets else data[
                "setKindId"]
            # Replace the kind value
            data["kindId"] = artifact_types.get(data["kindId"]).label if data["kindId"] in artifact_types else data[
                "kindId"]
            # Replace the primaryBonus.kind value
            data["primaryBonus"]["kind"] = artifact_stats.get(data['primaryBonus']['kind']).label if \
                data['primaryBonus']['kind'] in artifact_stats else data['primaryBonus']['kind']

            # add artifactStats key to the object
            data["allStats"] = {}
            primary_bonus = data["primaryBonus"]
            primary_value = primary_bonus["value"]
            if not primary_bonus["absolute"]:
                primary_value = primary_value * 100
            data["allStats"][stats_output(primary_bonus["kind"], primary_bonus["absolute"])] = primary_value

            # Iterate through the secondaryBonuses list
            for bonus in data["secondaryBonuses"]:
                # Replace the kind value
                bonus["kind"] = artifact_stats.get(bonus['kind']).label if bonus['kind'] in artifact_stats else bonus[
                    'kind']
                bonus_value = bonus["value"] + bonus["glyphPower"]
                if not bonus["absolute"]:
                    bonus_value = bonus_value * 100
                data["allStats"][stats_output(bonus["kind"], bonus["absolute"])] = bonus_value

            # # Filter data
            # # set flag to know if we hit the mark

            # search all artifacts level
            level_filter = True if len(level) == 0 else False
            if len(level) != 0 and data["level"] in level:
                level_filter = True

            # search all artifacts with the rank
            rank_filter = True if len(rank) == 0 else False
            if len(rank) != 0 and data["rank"] in rank_to_str(rank):
                rank_filter = True

            # search all artifacts with the rarity
            rarity_filter = True if len(rarity) == 0 else False
            if len(rarity) != 0 and data["rarity"] in rarity:
                rarity_filter = True

            # search all artifacts with the artifact_set
            set_filter = True if len(artifact_set) == 0 else False
            if len(artifact_set) != 0 and data["setKindId"] in artifact_set:
                set_filter = True

            # search all artifacts with the type
            type_filter = True if len(artifact_type) == 0 else False
            if len(artifact_type) != 0 and data["kindId"] in artifact_type:
                type_filter = True

            # Add artifact to search ones
            if level_filter and rank_filter and rarity_filter and set_filter and type_filter:
                searched_artifacts.append(data)

        # search all artifacts with the primary stats
        if len(primary_stat) != 0:
            primary_stats_filter = convert_to_stat_filter(primary_stat)
            searched_artifacts = [item for item in searched_artifacts if (item['primaryBonus']['kind'], item['primaryBonus']['absolute']) in primary_stats_filter]

        # search all artifacts with the substats
        if len(substat) != 0:
            substats_filter = convert_to_stat_filter(substat)
            searched_artifacts = [item for item in searched_artifacts if substats_filter.issubset(
                {(bonus['kind'], bonus['absolute']) for bonus in item['secondaryBonuses']}
            )]

            # Sort the data Ascending by the 'sort' keys in the "allStats" dictionary
        if len(sort) != 0:
            searched_artifacts = sorted(searched_artifacts, key=lambda x: tuple(x["allStats"].get(key, 0) for key in sort), reverse=True)

        if len(searched_artifacts) == 0:
            Console().print("No artifacts found with search criteria", style="bold red")
            exit()

        model = Artifacts.parse_obj(searched_artifacts)
        dto = convert_to_artifacts_dto(model)
        print(
            tabulate(
                dto.dict().get("__root__"),
                headers="keys",
                showindex="always",
                tablefmt="pretty",
                stralign="left",
            )
        )



def convert_to_stat_filter(stats: tuple) -> set:
    stat_filters = set()
    for value in stats:
        is_flat = True
        if "%" in value:
            value = value.replace("%", "")
            is_flat = False
        stat_filter = (value, is_flat)
        stat_filters.add(stat_filter)
    return stat_filters


def stats_output(stat: str, is_flat: bool) -> str:
    if not is_flat:
        return stat + "%"
    return stat


def rank_to_str(ranks: tuple) -> tuple:
    rank_mapping = {
        1: "One",
        2: "Two",
        3: "Three",
        4: "Four",
        5: "Five",
        6: "Six"
    }
    return tuple(rank_mapping.get(rank, "") for rank in ranks)

import asyncio

import click

from src.service.rtk_web_api import RTKWebApi
from src.utils import ln10, skills


@click.group()
def game() -> None:
    """
    Manages game resources
    """
    pass


@game.command()
@click.pass_context
def update_champion_index(ctx):
    """
    Get all accounts
    """
    asyncio.run(async_update_champion_index(ctx))


async def async_update_champion_index(ctx):
    # TODO This should be load through web API
    l10n = ln10()
    skills_index = skills()
    with RTKWebApi(ctx.obj["MOCK_WEBSOCKET_API"]) as web_api:
        champions_index = await web_api.client.StaticDataApi.get_hero_data()
        # Loop through the champion index and prepare data
        for hero_id, hero_data in champions_index.items():
            faction_placeholder = "l10n:hero/fraction?name={}#label"
            faction_ln10 = faction_placeholder.format(hero_data["faction"])
            faction = l10n[faction_ln10] if faction_ln10 in l10n else ""
            # Exception for NyresanElvess as it's not yet in locales
            if hero_data["faction"] == "NyresanElves":
                faction = "Sylvan Watchers"
            # the fully ascended champs with known faction
            # common which can't be ascended at all with known faction
            if (hero_data["ascended"] == 6 and faction != "") or (
                hero_data["rarity"] == "Common" and faction != ""
            ):
                hero_name = l10n[hero_data["name"]["key"]]
                short_hero_name = l10n[hero_data["shortName"]["key"]]
                leader_skill = hero_data["leaderSkill"]
                aura = ""
                if leader_skill is not None:
                    aura_template = l10n["l10n:leader-skill/description#label"]
                    # Leader Affinity
                    if leader_skill["affinity"] == "":
                        leader_affinity_ln10 = (
                            "l10n:leader-skill/allElements#label"
                        )
                    else:
                        leader_affinity_placeholder = (
                            "l10n:leader-skill/Element?id={}#label"
                        )
                        leader_affinity_ln10 = (
                            leader_affinity_placeholder.format(
                                leader_skill["affinity"]
                            )
                        )
                    leader_affinity = (
                        l10n[leader_affinity_ln10]
                        if leader_affinity_ln10 in l10n
                        else ""
                    )
                    # Leader Area
                    if leader_skill["area"] == "":
                        leader_area_ln10 = (
                            "l10n:leader-skill/allAreaTypes#label"
                        )
                    else:
                        leader_area_placeholder = (
                            "l10n:leader-skill/AreaTypeId?id={}#label"
                        )
                        leader_area_ln10 = leader_area_placeholder.format(
                            leader_skill["area"]
                        )
                    leader_area = (
                        l10n[leader_area_ln10]
                        if leader_area_ln10 in l10n
                        else ""
                    )
                    # Leader Skill
                    leader_skill_kind_placeholder = (
                        "l10n:leader-skill/StatKindId?id={}#label"
                    )
                    leader_skill_kind_ln10 = (
                        leader_skill_kind_placeholder.format(
                            leader_skill["kind"]
                        )
                    )
                    leader_skill_kind = (
                        l10n[leader_skill_kind_ln10]
                        if leader_skill_kind_ln10 in l10n
                        else ""
                    )
                    # Leader Skill Value
                    if not leader_skill["absolute"]:
                        leader_skill_value = (
                            str(int(leader_skill["value"] * 100)) + "%"
                        )
                    else:
                        leader_skill_value = int(leader_skill["value"])
                    aura = aura_template.format(
                        leader_skill_kind,
                        leader_area,
                        leader_affinity,
                        leader_skill_value,
                    )
                # Hero Skills
                for skill_type_id in hero_data["skillTypeIds"]:
                    print(f"skill_type_id {skill_type_id}")

                print(f"Hero {hero_id}: {hero_name} - {short_hero_name}")
                print(f"Faction {faction}")
                print(f"Aura {aura}")

        # json_string = json.dumps(champions_index, cls=json.JSONEncoder, indent=4)
        # # Print the JSON string
        # console = Console()
        # console.print(json_string)

        # Parse the data
        # all_accounts = Accounts.parse_obj(all_accounts)
        # rich.print_json(all_accounts.json())


#    champions_static = await client.StaticDataApi.get_hero_data()
# Serializing json
#    json_champions_static = json.dumps(champions_static, indent=4)
#    with open("heroes-index.json", "w") as outfile:
#        outfile.write(json_champions_static)

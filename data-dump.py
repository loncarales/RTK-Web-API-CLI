#!/usr/bin/env python3

import asyncio
from raidtoolkit import RaidToolkitClient
import json


async def main():
    client = RaidToolkitClient()
    client.connect()
    accounts = await client.AccountApi.get_accounts()

    # Account Dump
    account = await client.AccountApi.get_account_dump(accounts[0]["id"])
    # Serializing json
    json_account = json.dumps(account, indent=4)
    with open("account_dump.json", "w") as outfile:
        outfile.write(json_account)

    artifacts = await client.AccountApi.get_artifacts(accounts[0]["id"])
    # Serializing json
    json_artifacts = json.dumps(artifacts, indent=4)
    with open("artifacts.json", "w") as outfile:
        outfile.write(json_artifacts)

    champions = await client.AccountApi.get_heroes(accounts[0]["id"], False)
    # Serializing json
    json_champions = json.dumps(champions, indent=4)
    with open("champions.json", "w") as outfile:
        outfile.write(json_champions)

    # Static Data
    artifacts_static = await client.StaticDataApi.get_artifact_data()
    # Serializing json
    json_artifacts_static = json.dumps(artifacts_static, indent=4)
    with open("artifact-sets-index.json", "w") as outfile:
        outfile.write(json_artifacts_static)

    champions_static = await client.StaticDataApi.get_hero_data()
    # Serializing json
    json_champions_static = json.dumps(champions_static, indent=4)
    with open("heroes-index.json", "w") as outfile:
        outfile.write(json_champions_static)

    skills = await client.StaticDataApi.get_skill_data()
    # Serializing json
    json_skills = json.dumps(skills, indent=4)
    with open("skills-index.json", "w") as outfile:
        outfile.write(json_skills)

    localized_strings = await client.StaticDataApi.get_localized_strings()
    # Serializing json
    json_localisation = json.dumps(localized_strings, indent=4)
    with open("l10n-en.json", "w") as outfile:
        outfile.write(json_localisation)

    client.close()

if __name__ == "__main__":
    asyncio.run(main())

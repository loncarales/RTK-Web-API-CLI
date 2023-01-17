#!/usr/bin/env python3

import asyncio
from raidtoolkit import RaidToolkitClient
import json


async def main():
    client = RaidToolkitClient()
    client.connect()
    accounts = await client.AccountApi.get_accounts()

    # Account Data

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
    with open("artifacts-static.json", "w") as outfile:
        outfile.write(json_artifacts_static)

    champions_static = await client.StaticDataApi.get_hero_data()
    # Serializing json
    json_champions_static = json.dumps(champions_static, indent=4)
    with open("champions-static.json", "w") as outfile:
        outfile.write(json_champions_static)

    # Real Time API
    last_battle = await client.RealtimeApi.get_last_battle_response()
    # Serializing json
    json_last_battle = json.dumps(last_battle, indent=4)
    with open("last-battle.json", "w") as outfile:
        outfile.write(json_last_battle)

    client.close()

if __name__ == "__main__":
    asyncio.run(main())

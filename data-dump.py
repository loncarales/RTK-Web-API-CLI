#!/usr/bin/env python3

import asyncio
from raidtoolkit import RaidToolkitClient
import json


async def main():
    client = RaidToolkitClient()
    client.connect()
    accounts = await client.AccountApi.get_accounts()

    account = await client.AccountApi.get_account_dump(accounts[0]["id"])
    # Serializing json
    json_account = json.dumps(account, indent=4)
    with open("account.json", "w") as outfile:
        outfile.write(json_account)

    artifacts = await client.AccountApi.get_artifacts(accounts[0]["id"])
    # Serializing json
    json_artifacts = json.dumps(artifacts, indent=4)
    with open("artifacts.json", "w") as outfile:
        outfile.write(json_artifacts)

    client.close()

if __name__ == "__main__":
    asyncio.run(main())

#!/usr/bin/env python3

import asyncio
from raidtoolkit import RaidToolkitClient
import json


async def main():
    client = RaidToolkitClient()
    client.connect()
    accounts = await client.AccountApi.get_accounts()
    print(accounts)
    account = await client.AccountApi.get_account_dump(accounts[0]["id"])
    print(account)
    artifacts = await client.AccountApi.get_artifacts(accounts[0]["id"])
    # Serializing json
    json_artifacts = json.dumps(artifacts, indent=4)
    # Writing to data.json
    with open("artifacts.json", "w") as outfile:
        outfile.write(json_artifacts)
    client.close()

if __name__ == "__main__":
    asyncio.run(main())

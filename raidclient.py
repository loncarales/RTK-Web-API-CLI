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
    # Writing to data.json
    with open("account.json", "w") as outfile:
        outfile.write(json_account)
    client.close()

if __name__ == "__main__":
    asyncio.run(main())

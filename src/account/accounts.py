import asyncio

import click
from rich import print

from src.model.account import Accounts
from src.service.rtk_web_api import RTKWebApi


@click.group()
def accounts() -> None:
    """
    Manages accounts resources
    """
    pass


@accounts.command()
@click.pass_context
def get_all(ctx) -> None:
    """
    Get all accounts
    """
    asyncio.run(async_get_all(ctx))


async def async_get_all(ctx):
    with RTKWebApi(ctx.obj['MOCK_WEBSOCKET_API']) as web_api:
        all_accounts = await web_api.client.AccountApi.get_accounts()
        # Parse the data
        all_accounts = Accounts.parse_obj(all_accounts)
        print(all_accounts)

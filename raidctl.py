#!/usr/bin/env python3
import click
import tomli

from src.account.accounts import accounts
from src.artifact.artifacts import artifacts
from src.game.game import game


@click.group("cli")
@click.pass_context
def cli(ctx):
    """
    CLI for Raid Toolkit Web API
    """
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)
    ctx.ensure_object(dict)

    with open("config.toml", mode="rb") as fp:
        config = tomli.load(fp)
        ctx.obj['MOCK_WEBSOCKET_API'] = config["application"]["mock_websocket_api"]
    pass


cli.add_command(game)
cli.add_command(accounts)
cli.add_command(artifacts)


if __name__ == '__main__':
    cli(prog_name="raidctl.py")

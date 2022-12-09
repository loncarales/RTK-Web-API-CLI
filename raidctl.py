#!/usr/bin/env python3

import click
import json
from pygments import highlight
from pygments.formatters.terminal256 import Terminal256Formatter
from pygments.lexers.web import JsonLexer
from tabulate import tabulate

@click.group("cli")
def cli():
    """
    CLI for Raid Helper
    """
    pass


@cli.command("artifacts")
def artifacts():
    with open('data/celavko.json') as raid_json_file:
        parsed_json = json.load(raid_json_file)
        artifacts = []
        for artifact in parsed_json['artifacts']:
            artifact_id = artifact['id']
            artifact_rank = artifact['rank']
            artifact_level = artifact['level']
            artifact_rarity = artifact['rarity']
            artifact_set = artifact['setKind']
            artifact_peace = artifact['kind']
            artifact_main_stat = artifact['primaryBonus']['kind']
            artifact_main_stat_value = artifact['primaryBonus']['value']
            # Example sort by substat criticial rate for Weapon
            if artifact_peace == "Weapon":
                artifact_sub_stats = artifact['secondaryBonuses']
                for artifact_sub_stat in artifact_sub_stats:
                    artifact_sub_stat_kind = artifact_sub_stat['kind']
                    artifact_sub_stat_value = artifact_sub_stat['value']
                    artifact_sub_stat_level = artifact_sub_stat['level']
                    if artifact_sub_stat_kind == "CriticalChance":
                        artifact_dict = {
                            'id': artifact_id,
                            'set': artifact_set,
                            'peace': artifact_peace,
                            'rarity': artifact_rarity,
                            'rank': artifact_rank,
                            'level': artifact_level,
                            'mainStat': artifact_main_stat,
                            'mainValue': artifact_main_stat_value,
                            'subStat': "CriticalChance",
                            'subStatValue': artifact_sub_stat_value,
                            'subStatLevel': artifact_sub_stat_level
                        }
                        artifacts.append(artifact_dict)
        artifacts = sorted(artifacts, key=lambda item: item.get("subStatValue"), reverse=True)
        # colorize_json(artifacts)
        click.echo(
            tabulate(
                artifacts,
                headers="keys",
                showindex="always",
                tablefmt="pretty",
                stralign="left",
            )
        )

def colorize_json(json_content):
    """ Colorize JSON serialized string and dumps it to console

    Args:
        json_content (str): JSON serialized string
    """
    raw_json = json.dumps(json_content, indent=4)
    colorful_json = highlight(raw_json, lexer=JsonLexer(), formatter=Terminal256Formatter())
    click.echo(colorful_json)


def main():
    cli(prog_name="raidctl.py")


if __name__ == '__main__':
    main()

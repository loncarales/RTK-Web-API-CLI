# CLI for Raid Toolkit Web API

The main purpose of this tool is just a POC (proof of concept) for showing my kids how we can use an SDK (Software 
development kit) to create a new tool. 
This is a CLI script which access the [Raid Toolkit](https://raidtoolkit.com/) Web API 
for accessing the [Raid: Shadow Legends](https://raidshadowlegends.com/) game data. Currently, it queries the artifacts 
and does some basic data manipulation (filtering and sorting [by stats]).

This is example of very basic usage which could be extended to perform more powerful operations like search permutations, 
finding the best "equipment" for champions or identifying the "crappy" items.

## Prerequisites

Before you begin, ensure you have met the following requirements:

The 'Python' script will run on any OS with Python installed. RTK (Raid Toolkit) is only supported on Windows 10 or Windows 11. 
You will also need to have a Raid Shadow Legends installed via [Plarium Play](https://plarium.com/). The Python script accessing the RTK 
bust be run on the same computer as RTK. Cross-network access is not a supported scenario. RTK provides a WEB API exposed via 
WebSocket (wss://localhost:9090) and can be accessed via browser or a script, in this case the script is written in Python. 

* You have installed the [Python](https://www.python.org/) at least version `3.10`
* You have installed the [Poetry](https://python-poetry.org/) for dependency management
* You have RTK and Raid: Shadow Legends installed

## Installing the tool

### Clone this repository

```bash
git clone https://github.com/loncarales/RTK-Web-API-CLI.git
```

### Configuring application

There is no additional configuration needed. There is only one flag set in `config.toml` file, that allows us to use the
application code in `development` environment without a need to have RTK installed. When the value of `mock_websocket_api`
is set to `true` the  Web API will be `mocked`. The data is read locally from the JSON files which were previously 
exported from the game.  

```toml
[application]
  mock_websocket_api = false
```

### Before running the application

First we need to install the Python dependencies for the project. Use the following command

```bash
poetry install
```

Next we need to activate the virtual environment. The easiest way to create the virtual environment is to create a new shell 
using the `poetry shell` command. To deactivate a virtual environment and exist from the shell, use the `exit` command.

### Running the application

Running just a script with `python ./raidctl.py` will dump a help message

```bash
python ./raidctl.py 

Usage: raidctl.py [OPTIONS] COMMAND [ARGS]...

  CLI for Raid Toolkit Web API

Options:
  --help  Show this message and exit.

Commands:
  accounts   Manages accounts resources
  artifacts  Manages artifacts resources
```

### Example query

Let's search for artifacts:

- type: Boots
- rank: 5 or 6
- rarity: Legendary or Epic
- primary stat: SPD
- substat: ACC

and sort them by ACC Desc

```bash
python ./raidctl.py artifacts get-all -at Boots -r 4 -r 5 -ra Legendary -ra Epic -ps SPD -su ACC --sort ACC

accessing RTK via client
+---+------+---------------+-------+-------+------+-----------+--------------+----------------------------------------------------------------------+
|   | id   | set           | type  | level | rank | rarity    | primary_stat | substats                                                             |
+---+------+---------------+-------+-------+------+-----------+--------------+----------------------------------------------------------------------+
| 0 | 5161 | Perception    | Boots | 16    | 5    | Epic      | SPD 40       | {'ATK(1)': '10%+1%', 'ACC(1)': '22+2', 'DEF': '15+5'}                |
| 1 | 7635 | Lifesteal     | Boots | 0     | 5    | Epic      | SPD 5        | {'RES': '11', 'ACC': '11', 'C. DMG': '5%'}                           |
| 2 | 1605 | Perception    | Boots | 16    | 4    | Epic      | SPD 35       | {'RES(2)': '23+2', 'C. RATE(1)': '9%', 'ACC': '7+2', 'C. DMG': '4%'} |
| 3 | 5604 | Critical Rate | Boots | 0     | 5    | Epic      | SPD 5        | {'HP': '397', 'ACC': '8', 'DEF': '16'}                               |
| 4 | 6479 | Perception    | Boots | 0     | 4    | Legendary | SPD 4        | {'ACC': '8', 'DEF': '13', 'ATK': '7', 'RES': '7'}                    |
+---+------+---------------+-------+-------+------+-----------+--------------+----------------------------------------------------------------------+
```

You can see all input options if you add `--help` to the command line

```bash
Usage: raidctl.py artifacts get-all [OPTIONS]

  Get all Artifacts based on input options

Options:
  -l, --level INTEGER        Filter by the artifact level
  -r, --rank INTEGER         Filter by the artifact rank
  -ra, --rarity TEXT         Filter by the artifact rarity
  -as, --artifact-set TEXT   Filter by the artifact set
  -at, --artifact-type TEXT  Filter by the artifact type
  -ps, --primary-stat TEXT   Filter by the artifact primary stat
  -su, --substat TEXT        Filter by the artifact substat
  -s, --sort TEXT            Sort artifacts by any stat
  --help                     Show this message and exit.
```

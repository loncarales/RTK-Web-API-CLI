from raidtoolkit import RaidToolkitClient
from rich.console import Console

from src.mockraidtoolkit.mock_raid_toolkit import MockRaidToolkitClient


class RTKWebApi:
    def __init__(self, mock_websocket_api: bool):
        self.mock_websocket_api = mock_websocket_api

    def __enter__(self):
        if self.mock_websocket_api:
            Console().print("access to RTK is mocked", style="blue")
            self.client = MockRaidToolkitClient()
            self.client.connect()
        else:
            Console().print("accessing RTK via client", style="green")
            self.client = RaidToolkitClient()
            self.client.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.client.close()
        pass

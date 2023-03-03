from src.mockraidtoolkit.local_api_client import LocalApiClient


class StaticDataApi:
    def __init__(self, client: LocalApiClient):
        self.client = client

    def get_hero_data(self):
        return self.client.call("game-data", "heroes-index.json", "heroTypes")

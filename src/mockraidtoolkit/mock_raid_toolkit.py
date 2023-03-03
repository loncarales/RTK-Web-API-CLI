from src.mockraidtoolkit.account_api import AccountApi
from src.mockraidtoolkit.local_api_client import LocalApiClient
from src.mockraidtoolkit.static_data_api import StaticDataApi


class MockRaidToolkitClient:
    """Provides MOCK access to Raid Toolkit APIs"""

    def __init__(self):
        self.client = LocalApiClient()

    @property
    def AccountApi(self):
        return AccountApi(self.client)

    @property
    def StaticDataApi(self):
        return StaticDataApi(self.client)

    def connect(self):
        self.client.connect()

    def close(self):
        self.client.close()

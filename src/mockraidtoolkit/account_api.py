from src.mockraidtoolkit.local_api_client import LocalApiClient


class AccountApi:
    def __init__(self, client: LocalApiClient):
        self.client = client

    def get_accounts(self):
        return self.client.call("json-data", "accounts.json", "")

    def get_artifacts(self, account_id: str):
        return self.client.call(
            "json-data", "artifacts.json", "", [account_id]
        )

from src.utils import read_json_data


class LocalApiClient:
    """Provides access to Local APIs"""

    def connect(self):
        pass

    def close(self):
        pass

    async def call(self, file_path: str, file_name: str, json_key: str, args=[]):
        return await read_json_data(file_path, file_name, json_key)

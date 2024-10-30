import os
from typing import Optional, Dict, Any

import httpx


class ApiClient:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.headers = {"Authorization": f"Token {token}"}

    async def get(self, endpoint: str) -> Optional[Dict[str, Any]]:
        url = f"{self.base_url}/{endpoint}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.json()
            print(
                f"Error getting data from {url}: {response.status_code}, {response.text}"
            )
            return None

    async def post(self, endpoint: str, payload: Dict[str, Any]) -> bool:
        url = f"{self.base_url}/{endpoint}"
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=self.headers)
            if response.status_code == 201:
                print("Data posted successfully")
                return True
            print(
                f"Error posting data to {url}: {response.status_code}, {response.text}"
            )
            return False


api_client = ApiClient(base_url=os.getenv("API_URL"), token=os.getenv("API_TOKEN"))

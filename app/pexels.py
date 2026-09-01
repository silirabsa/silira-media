import os
from typing import Any

import httpx

PEXELS_API_URL = "https://api.pexels.com/v1"


def _headers() -> dict[str, str]:
    api_key = os.getenv("PEXELS_API_KEY")
    if not api_key:
        raise RuntimeError("PEXELS_API_KEY is not configured")
    return {"Authorization": api_key}


async def search_photos(query: str, page: int = 1, per_page: int = 18) -> dict[str, Any]:
    params = {"query": query, "page": page, "per_page": min(per_page, 80)}
    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(f"{PEXELS_API_URL}/search", params=params, headers=_headers())
        response.raise_for_status()
        return response.json()


async def search_videos(query: str, page: int = 1, per_page: int = 18) -> dict[str, Any]:
    params = {"query": query, "page": page, "per_page": min(per_page, 80)}
    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(f"{PEXELS_API_URL}/videos/search", params=params, headers=_headers())
        response.raise_for_status()
        return response.json()

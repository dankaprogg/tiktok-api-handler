from asyncio import iscoroutinefunction
from functools import wraps
from typing import Dict, List, Optional

from tiktok.user import User

import aiohttp
import urllib

tiktok_api_url = "https://m.tiktok.com/api"
tiktok_api_search_url = f"{tiktok_api_url}/search/general/full"

class TikTok:
    def __init__(self):
        self._session: aiohttp.ClientSession = None

        self.cookies: Dict = { "ttwid": None }
        self.headers: Dict = {
            "user-agent": "5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1"
        }

        def check_session(cls, func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                if cls._session is None:
                    await cls._setup_session()

                return await func(*args, **kwargs)
                
            return wrapper

        for name in dir(self):
            obj = getattr(self, name)
            if iscoroutinefunction(obj) and not name.startswith("_"):
                setattr(self, name, check_session(self, obj))

    async def _setup_session(self):
        self._session = aiohttp.ClientSession()
        async with self._session.head("https://www.tiktok.com", headers=self.headers) as response:
            self.cookies.update(response.cookies)

    async def close(self):
        await self._session.close()

    async def get_user(self, username: str, unique_value: Optional[bool] = True) -> (User | List[User]):
        result = []

        if not username.startswith("@"):
            username = f"@{username}"

        async with self._session.get(
            f"{tiktok_api_search_url}/?keyword={urllib.parse.quote(username)}",
            cookies=self.cookies,
            headers=self.headers
        ) as response:
            if response.ok:
                data = await response.json()
                message = data.get("status_msg")
                if message:
                    raise Exception(message)
                else:
                    for item in data["data"]:
                        if item["type"] == 4:
                            for _user in item["user_list"]:
                                user = User(**_user["user_info"])
                                if user.unique_id == username.replace("@", ""):
                                    if unique_value:
                                        return user

                                    result.append(user)

        return result or None
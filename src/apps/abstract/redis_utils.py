# Python
import pickle
from typing import Any

# Local
from src.settings.base import aioredis


class RedisUtils:
    """Utils for Cache in Redis."""

    async def a_set_to_redis(
        self, key: str, value: Any, ttl: int = 60*30
    ) -> None:
        obj = pickle.dumps(obj=value)
        await aioredis.set(name=key, value=obj, ex=ttl)
        return
    
    async def a_get_from_redis(self, key: str) -> Any|None:
        try:
            obj = await aioredis.get(name=key)
            value = pickle.loads(obj)
            return value
        except:
            return None

    async def a_remove_key_from_redis(self, key: str) -> None:
        await aioredis.delete(key)
        return
    
    
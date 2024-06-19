# FastAPI
from fastapi import FastAPI

# SQL
from sqlalchemy.ext.asyncio import (
    create_async_engine, async_sessionmaker,
)

# Third-Party
import redis

# Python
import logging

# Local
from .const import DEBUG, REDIS_URL, DB_URL


app = FastAPI(title="Reminder", debug=DEBUG)
engine = create_async_engine(url=DB_URL)
session = async_sessionmaker(
    bind=engine, expire_on_commit=True,
)
pool = redis.asyncio.ConnectionPool.from_url(url=REDIS_URL)
aioredis = redis.asyncio.Redis(connection_pool=pool)
logger = logging.getLogger(__name__)
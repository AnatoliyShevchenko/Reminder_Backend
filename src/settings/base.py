# FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
app.add_middleware(
    middleware_class=CORSMiddleware, 
    allow_origins=["http://127.0.0.1"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "PUT", "DELETE"],
    allow_headers=[
        "Accept", "Accept-Language", "Content-Language", "Content-Type"
    ]
)
engine = create_async_engine(url=DB_URL)
session = async_sessionmaker(
    bind=engine, expire_on_commit=True,
)
pool = redis.asyncio.ConnectionPool.from_url(url=REDIS_URL)
aioredis = redis.asyncio.Redis(connection_pool=pool)
logger = logging.getLogger(__name__)


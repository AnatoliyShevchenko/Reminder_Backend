# Third-Party
from decouple import config


# App
DEBUG = config("DEBUG", cast=bool)
SECRET_KEY = config("SECRET_KEY")
ADMIN_ID = config("ADMIN_ID", cast=int)

# Postgres
DB_NAME = config("DB_NAME")
DB_USER = config("DB_USER")
DB_PASS = config("DB_PASS")
DB_HOST = config("DB_HOST")
DB_PORT = config("DB_PORT")
DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Redis
REDIS_PROTOCOL = config("REDIS_PROTOCOL")
REDIS_HOST = config("REDIS_HOST")
REDIS_PORT = config("REDIS_PORT")
REDIS_URL = f"{REDIS_PROTOCOL}{REDIS_HOST}:{REDIS_PORT}"


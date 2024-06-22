# Third-Party
from passlib.hash import pbkdf2_sha256
import jwt

# Python
from datetime import datetime, timedelta

# Local
from src.settings.const import SECRET_KEY
from .models import Users


def make_password(password: str):
    temp = pbkdf2_sha256.hash(secret=password)
    return temp

def verify_password(password: str, hash_password: str):
    temp = pbkdf2_sha256.verify(secret=password, hash=hash_password)
    return temp

def create_access_token(user: Users):
    expire = datetime.now() + timedelta(minutes=30)
    data = {
        "username":user.username,
        "hashed_password":user.password,
        "exp":expire
    }
    token = jwt.encode(payload=data, key=SECRET_KEY)
    return token


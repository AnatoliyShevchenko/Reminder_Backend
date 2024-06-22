# FastAPI
from fastapi import HTTPException, status, Request

# Third-Party
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
import jwt

# Python
from datetime import datetime

# Local
from .schemas import CreateAdminSchema
from src.settings.const import ADMIN_ID, SECRET_KEY


async def check_admin(obj: CreateAdminSchema):
    data = CreateAdminSchema.model_validate(obj=obj)
    if data.telegram_id != ADMIN_ID:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="You're not admin."
        )
    return data

async def check_token(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="token required"
        )
    data: dict = jwt.decode(jwt=token, key=SECRET_KEY)
    date = data.get("exp")
    if date < datetime.now():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="token expired!"
        )
    return True


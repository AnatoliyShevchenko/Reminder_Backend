# FastAPI
from fastapi import APIRouter, status, Response, HTTPException, Depends

# Local
from src.apps.abstract.schemas import ResponseSchema
from src.apps.abstract.redis_utils import RedisUtils
from .schemas import (
    UserSchema, UsersSchema, CreateUserSchema, 
    CreateAdminSchema, AuthsSchema, TokenSchema,
)
from .orm import UsersOrm
from .auths import make_password, verify_password, create_access_token
from .depends import check_admin


class AdminView:
    """View for Admin."""

    def __init__(self) -> None:
        self.path = "/admin"
        self.orm = UsersOrm()
        self.router = APIRouter(prefix="/api/v1")
        self.router.add_api_route(
            path=self.path+"/reg", endpoint=self.register, methods=["POST"], 
            responses={
                200: {"model": ResponseSchema},
                400: {"model": ResponseSchema},
                403: {"model": None}
            }
        )
        self.router.add_api_route(
            path=self.path+"/auth", endpoint=self.auth, methods=["POST"], 
            responses={
                200: {"model": TokenSchema},
                400: {"model": ResponseSchema}
            }
        )

    async def register(
        self, response: Response, 
        obj: CreateAdminSchema = Depends(check_admin)
    ):
        """Admin registration will be executed in bot."""
        is_success: bool = await self.orm.register_admin(
            telegram_id=obj.telegram_id, username=obj.username,
            hash_password=make_password(password=obj.password),
            timezone=obj.timezone, language=obj.language
        )
        if is_success:
            return ResponseSchema(response="Admin registered success!")
        response.status_code=status.HTTP_400_BAD_REQUEST
        return ResponseSchema(
            response="For some reasons we can't register you!"
        )
    
    async def auth(self, obj: AuthsSchema, resonse: Response):
        """This will be in a frontend(admin panel)."""
        data = AuthsSchema.model_validate(obj=obj)
        admin = await self.orm.get_admin(username=data.username)
        if not admin:
            resonse.status_code=status.HTTP_400_BAD_REQUEST
            return ResponseSchema(
                response=f"User {data.username} is not found"
            )

        validate = verify_password(
            password=data.password, hash_password=admin.password
        )
        if not validate:
            resonse.status_code=status.HTTP_400_BAD_REQUEST
            return ResponseSchema(
                response="incorrect password"
            )
        token = create_access_token(user=admin)
        return TokenSchema(access_token=token)


class UsersView(RedisUtils):
    """View for Users."""

    def __init__(self) -> None:
        self.path = "/users"
        self.orm = UsersOrm()
        self.router = APIRouter(prefix="/api/v1")
        self.router.add_api_route(
            path=self.path, endpoint=self.get, methods=["GET"], 
            responses={
                200: {"model": UsersSchema},
                400: {"model": None}
            }
        )
        self.router.add_api_route(
            path=self.path+"/{telegram_id}", endpoint=self.retrieve, 
            methods=["GET"], responses={
                200: {"model": ResponseSchema},
                400: {"model": ResponseSchema}
            }
        )
        self.router.add_api_route(
            path=self.path, endpoint=self.post, methods=["POST"], 
            responses={
                200: {"model": ResponseSchema},
                400: {"model": ResponseSchema}
            }
        )

    async def get(self):
        key = "all_users"
        users = await self.a_get_from_redis(key=key)
        if not users:
            users = await self.orm.get_all_users()
            if not users:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail="no users founded"
                )
            await self.a_set_to_redis(key=key, value=users)
        temp = [i.__dict__ for i in users]
        schema = UsersSchema(response=temp)
        return schema
    
    async def retrieve(self, telegram_id: int):
        key = f"user_{telegram_id}"
        data = await self.a_get_from_redis(key=key)
        if not data:
            data = await self.orm.get_user(telegram_id=telegram_id)
            if not data:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
            await self.a_set_to_redis(key=key, value=data)
        return UserSchema.model_validate(obj=data.__dict__)

    async def post(self, obj: CreateUserSchema, response: Response):
        data = CreateUserSchema.model_validate(obj=obj)
        created = await self.orm.create_user(
            telegram_id=data.telegram_id, timezone=data.timezone,
            language=data.language
        )
        if not created:
            response.status_code=status.HTTP_400_BAD_REQUEST
            return ResponseSchema(response="For some reasons we can't register you")
        await self.a_remove_key_from_redis(key="all_users")
        return ResponseSchema(response="Success")
    

admins = AdminView()
users = UsersView()


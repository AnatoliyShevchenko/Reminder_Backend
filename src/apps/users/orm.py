# SQLAlchemy
from sqlalchemy import select, update, delete, and_

# Local
from src.settings.base import session, logger
from src.settings.const import ADMIN_ID
from .models import Users


class UsersOrm:
    """ORM utils for Users model."""

    async def register_admin(
        self, telegram_id: int, username: str, 
        hash_password: str, timezone: int, language: str
    ) -> bool:
        if telegram_id == ADMIN_ID:
            try:
                async with session() as conn:
                    async with conn.begin():
                        obj = Users(
                            telegram_id=telegram_id, username=username,
                            password=hash_password, timezone=timezone,
                            language=language
                        )
                        await conn.add(instance=obj)
                        await conn.commit()
                    await conn.aclose()
                return True
            except Exception as e:
                logger.error(msg="Cannot register user:", exc_info=e)
                return False
        else:
            return False

    async def get_user(self, telegram_id: int):
        async with session() as conn:
            user = await conn.execute(select(Users).where(
                Users.telegram_id == telegram_id
            ))
            result = user.scalar_one_or_none()
            await conn.aclose()
        return result
    
    async def get_admin(self, username: str):
        async with session() as conn:
            user = await conn.execute(select(Users).where(
                Users.username == username
            ))
            result = user.scalar()
            await conn.aclose()
        return result
    
    async def get_all_users(self):
        async with session() as conn:
            users = await conn.execute(select(Users))
            result = users.scalars().fetchall()
            await conn.aclose()
        return result
    
    async def create_user(
        self, telegram_id: int, timezone: int, language: str
    ):
        try:
            async with session() as conn:
                async with conn.begin():
                    obj = Users(
                        telegram_id=telegram_id, timezone=timezone,
                        language=language
                    )
                    conn.add(instance=obj)
                    await conn.commit()
                await conn.aclose()
            return True
        except Exception as e:
            logger.error(msg="Cannot register user:", exc_info=e)
            return False
        
    async def change_timezone(self, telegram_id: int, timezone: int):
        try:
            async with session() as conn:
                async with conn.begin():
                    stmt = update(Users).where(
                        Users.telegram_id == telegram_id
                    ).values(timezone=timezone)
                    await conn.execute(statement=stmt)
                    await conn.commit()
                await conn.aclose()
            return True
        except Exception as e:
            logger.error(msg="Cannot change timezone:", exc_info=e)
            return False
        
    async def remove_user(self, telegram_id: int):
        try:
            async with session() as conn:
                async with conn.begin():
                    stmt = delete(Users).where(Users.telegram_id == telegram_id)
                    await conn.execute(statement=stmt)
                    await conn.commit()
                await conn.aclose()
            return True
        except Exception as e:
            logger.error(msg="Cannot remove user:", exc_info=e)
            return False
        

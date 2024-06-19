# SQLAlchemy
from sqlalchemy import select, update, delete, and_

# Python
from datetime import datetime, timedelta

# Local
from src.settings.base import session, logger
from .models import Events


class EventsOrm:
    """ORM utils for Events."""

    async def get_active_user_events(self, telegram_id: int):
        async with session() as conn:
            users = await conn.execute(select(Events).where(
                and_(
                    Events.telegram_id == telegram_id, 
                    Events.is_finished == False
            )))
            result = users.scalars().fetchall()
            await conn.aclose()
        return result
    
    async def remove_eldest_events(self):
        to_remove = datetime.now() - timedelta(days=2)
        async with session() as conn:
            async with conn.begin():
                stmt = delete(Events).where(
                    Events.date <= to_remove
                )
                await conn.execute(statement=stmt)
                await conn.commit()
            await conn.aclose()
        return True

    async def create_event(
        self, telegram_id: int, title: str, date: datetime
    ):
        async with session() as conn:
            async with conn.begin():
                obj = Events(
                    title=title, date=date, is_finished=False,
                    telegram_id=telegram_id
                )
                conn.add(instance=obj)
                await conn.commit()
            await conn.aclose()
        return True

    async def update_event(
        self, event_id: int, title: str, date: datetime
    ):
        pass
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
            events = await conn.execute(select(Events).where(
                and_(
                    Events.telegram_id == telegram_id, 
                    Events.is_finished == False
            )))
            result = events.scalars().fetchall()
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
        try:
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
        except Exception as e:
            logger.error(msg="Cannot create event:", exc_info=e)
            return False

    async def update_event(
        self, event_id: int, title: str, date: datetime
    ):
        try:
            async with session() as conn:
                async with conn.begin():
                    stmt = update(Events).where(and_(
                        Events.id == event_id, 
                        Events.is_finished == False
                    )).values(title=title, date=date)
                    await conn.execute(statement=stmt)
                    await conn.commit()
                await conn.aclose()
            return True
        except Exception as e:
            logger.error(msg="Cannot update event:", exc_info=e)
            return False
        
    async def finish_event(self, event_id):
        try:
            async with session() as conn:
                async with conn.begin():
                    stmt = update(Events).where(and_(
                        Events.id == event_id, 
                        Events.is_finished == False
                    )).values(is_finished=True)
                    await conn.execute(statement=stmt)
                    await conn.commit()
                await conn.aclose()
            return True
        except Exception as e:
            logger.error(msg="Cannot finish event:", exc_info=e)
            return False
        
    async def get_event(self, event_id: int):
        async with session() as conn:
            users = await conn.execute(select(Events).where(
                and_(
                    Events.id == event_id, 
                    Events.is_finished == False
            )))
            result = users.scalar_one_or_none()
            await conn.aclose()
        return result
    
    
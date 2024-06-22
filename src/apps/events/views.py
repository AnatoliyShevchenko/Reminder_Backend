# FastAPI
from fastapi import APIRouter, status, HTTPException

# Local
from src.apps.abstract.schemas import ResponseSchema
from src.apps.abstract.redis_utils import RedisUtils
from .schemas import EventSchema, EventsSchema, CreateEventSchema
from .orm import EventsOrm


class EventsView(RedisUtils):
    """View for Events."""

    def __init__(self) -> None:
        self.path = "/events"
        self.orm = EventsOrm()
        self.router = APIRouter(prefix="/api/v1")
        self.router.add_api_route(
            path=self.path+"/{telegram_id}", endpoint=self.get, 
            methods=["GET"], responses={
                200: {"model": EventsSchema},
                400: {"model": None}
            }
        )
        self.router.add_api_route(
            path=self.path, endpoint=self.post, 
            methods=["POST"], responses={
                200: {"model": ResponseSchema},
                400: {"model": None}
            }
        )
        self.router.add_api_route(
            path=self.path+"/{event_id}", endpoint=self.put, 
            methods=["PUT"], responses={
                200: {"model": ResponseSchema},
                400: {"model": None}
            }
        )
        self.router.add_api_route(
            path=self.path+"/{event_id}", endpoint=self.patch, 
            methods=["PATCH"], responses={
                200: {"model": ResponseSchema},
                400: {"model": None}
            }
        )
        self.router.add_api_route(
            path=self.path+"/{event_id}", endpoint=self.retrieve, 
            methods=["GET"], responses={
                200: {"model": ResponseSchema},
                400: {"model": None}
            }
        )

    async def get(self, telegram_id: int):
        key = f"events_of_{telegram_id}"
        events = await self.a_get_from_redis(key=key)
        if not events:
            events = await self.orm.get_active_user_events(
                telegram_id=telegram_id
            )
            if not events:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail="no events founded"
                )    
            await self.a_set_to_redis(key=key, value=events)
        temp = [i.__dict__ for i in events]
        schema = EventsSchema(response=temp)
        return schema
        
    async def post(self, obj: CreateEventSchema):
        data = CreateEventSchema.model_validate(obj=obj)
        created = await self.orm.create_event(
            telegram_id=data.telegram_id, 
            title=data.title, date=data.date
        )
        if not created:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="for some reasons we can't create your event"
            )
        await self.a_remove_key_from_redis(
            key=f"events_of_{data.telegram_id}"
        )
        return ResponseSchema(response="Success")
    
    async def put(self, event_id: int, obj: CreateEventSchema):
        data = CreateEventSchema.model_validate(obj=obj)
        updated = await self.orm.update_event(
            event_id=event_id, title=data.title, date=data.date
        )
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="for some reasons we can't update your event"
            )
        await self.a_remove_key_from_redis(
            key=f"events_of_{data.telegram_id}"
        )
        return ResponseSchema(response="Success")

    async def patch(self, event_id: int):
        finished = await self.orm.finish_event(event_id=event_id)
        if not finished:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="for some reasons we can't finish your event"
            )
        return ResponseSchema(response="Success")
        
    async def retrieve(self, event_id: int):
        key = f"event_{event_id}"
        data = await self.a_get_from_redis(key=key)
        if not data:
            data = await self.orm.get_event(event_id=event_id)
            if not data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail=f"there is no events with id {event_id}"
                )
            await self.a_set_to_redis(key=key, value=data)
        return EventSchema.model_validate(obj=data.__dict__)
    

events = EventsView()


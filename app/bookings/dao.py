from datetime import date
import select
from sqlalchemy import and_, func, insert, or_
from app.dao.base import BaseDAO
from app.bookings.models import Bookings
from app.database import async_session_maker
from app.exceptions import RoomFullyBookedException
from app.hotels.rooms.models import Rooms
from app.users.models import Users


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add(cls, user: Users, room_id: int, date_from: date, date_to: date):
        async with async_session_maker() as session:
            booked_rooms = select(cls.model).where(
                and_(
                    cls.model.room_id == room_id, 
                    or_(
                        and_(
                            Bookings.date_from >= date_from, 
                            Bookings.date_to <= date_to
                        ),
                        and_(
                            Bookings.date_from <= date_to, 
                            Bookings.date_to > date_from
                        )
                    )
                )
            ).cte('booked_rooms')

            rooms_left = select(
                Rooms.rooms_quantity - func.count(booked_rooms.c.room_id).label('rooms_left')).select_from(
                    Rooms
                ).outerjoin(
                    booked_rooms, booked_rooms.c.room_id == Rooms.id
                ).where(
                    Rooms.id == room_id
                ).group_by(
                    Rooms.quantity, booked_rooms.c.room_id
                )
            
            result = await session.execute(select(rooms_left).limit(1))
            room_left = result.scalar_one_or_none()
            if not room_left:
                raise RoomFullyBookedException
            
            print(result.mappings().all())
from datetime import date
from sqlalchemy import and_, func, insert, or_, select
from app.dao.base import BaseDAO
from app.bookings.models import Bookings
from app.database import async_session_maker
from app.exceptions import RoomFullyBookedException
from app.hotel.models import Rooms
from app.users.models import Users


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    def rooms_left_cte(cls, date_from: date, date_to: date):
        '''Возвращает CTE для подсчета свободных комнат (не выполняет запрос)'''
        booked_rooms = select(
            cls.model.room_id, 
            func.count(cls.model.room_id).label('booked_rooms')
        ).where(
            or_(
                and_(
                    Bookings.date_to <= date_to, 
                    Bookings.date_to >= date_from
                ),
                and_(
                    Bookings.date_from <= date_to, 
                    Bookings.date_from >= date_from
                ),
                and_(
                    Bookings.date_from <= date_from, 
                    Bookings.date_to >= date_to
                )
            )
        ).group_by(cls.model.room_id).cte('booked_rooms')
        
        rooms_left = select(
            Rooms.id, 
            Rooms.hotel_id,
            (Rooms.quantity - func.coalesce(booked_rooms.c.booked_rooms, 0)).label('rooms_left')
        ).select_from(
            Rooms
        ).outerjoin(
            booked_rooms, booked_rooms.c.room_id == Rooms.id
        ).cte('rooms_left')
        
        return rooms_left

    @classmethod
    async def rooms_left(cls, date_from: date, date_to: date):
        '''Количество свободных комнат (возвращает список словарей)'''
        async with async_session_maker() as session:
            rooms_left_cte = cls.rooms_left_cte(date_from, date_to)
            query = select(rooms_left_cte)
            result = await session.execute(query)
            result = result.mappings().all()
            return result


    @classmethod
    async def add(cls, user: Users, room_id: int, date_from: date, date_to: date):
        '''Добавление бронирования'''
        rooms_left_list = await cls.rooms_left(date_from, date_to)
        
        async with async_session_maker() as session:
            rooms_left = None
            for room in rooms_left_list:
                if room['id'] == room_id:
                    rooms_left = room['rooms_left']
                    break
            
            if rooms_left is None or rooms_left <= 0:
                raise RoomFullyBookedException

            get_price = select(Rooms.price).where(Rooms.id == room_id)
            price = await session.execute(get_price)
            price = price.scalar()
            
            add_booking = insert(Bookings).values(
                room_id=room_id,
                user_id=user.id,
                date_from=date_from,
                date_to=date_to,
                price=price
            ).returning(Bookings)
            new_booking = await session.execute(add_booking)
            await session.commit()
            return new_booking.scalar()
            
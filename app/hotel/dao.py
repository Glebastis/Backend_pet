from datetime import date
from sqlalchemy import func, select
from app.dao.base import BaseDAO
from app.bookings.dao import BookingDAO
from app.hotel.models import Hotel, Rooms
from app.database import async_session_maker
from app.hotel.schemas import SHotel, SRoom


class HotelDAO(BaseDAO):
    model = Hotel
    rooms_model = Rooms
    
    @classmethod
    async def get_hotels_list_by_region(cls, location: str, date_from: date, date_to: date):
        '''Получение списка отелей с количеством свободных комнат'''
        async with async_session_maker() as session:
            # Используем CTE из BookingDAO для подсчета свободных комнат
            rooms_left = BookingDAO.rooms_left_cte(date_from, date_to)
            
            # CTE для получения отелей с суммой свободных комнат
            # rooms_left уже содержит все комнаты с подсчитанными свободными местами
            hotels_rooms_sum = select(
                rooms_left.c.hotel_id,
                func.sum(rooms_left.c.rooms_left).label('rooms_quantity')
            ).group_by(
                rooms_left.c.hotel_id
            ).having(
                func.sum(rooms_left.c.rooms_left) > 0
            ).cte('hotels_rooms_sum')
            
            # Основной запрос: отели с суммой свободных комнат
            hotels_with_free_rooms = select(
                cls.model.id,
                cls.model.name,
                cls.model.location,
                cls.model.services,
                hotels_rooms_sum.c.rooms_quantity,
                cls.model.image_id
            ).select_from(
                cls.model
            ).join(
                hotels_rooms_sum, cls.model.id == hotels_rooms_sum.c.hotel_id
            ).where(
                cls.model.location.contains(location)
            )
            
            result = await session.execute(hotels_with_free_rooms)
            result = result.mappings().all()
            return [SHotel.model_validate(hotel) for hotel in result]

    @classmethod
    async def get_rooms_by_hotel_id(cls, hotel_id: int, date_from: date, date_to: date):
        '''Получение списка комнат по id отеля'''
        async with async_session_maker() as session:
            rooms_left = BookingDAO.rooms_left_cte(date_from, date_to)
            rooms_info = select(
                cls.rooms_model.id,
                cls.rooms_model.name,
                cls.rooms_model.price,
                cls.rooms_model.services,
                cls.rooms_model.image_id,
                rooms_left.c.rooms_left
            ).select_from(
                cls.rooms_model
            ).join(rooms_left, cls.rooms_model.id == rooms_left.c.id).where(rooms_left.c.hotel_id == hotel_id)
            result = await session.execute(rooms_info)
            result = result.mappings().all()
            return [SRoom.model_validate(room) for room in result]

    @classmethod
    async def get_hotel_by_id(cls, hotel_id: int):
        '''Получение отеля по id'''
        async with async_session_maker() as session:
            hotel = select(cls.model).where(cls.model.id == hotel_id)
            result = await session.execute(hotel)
            result = result.scalar_one_or_none()
            return SHotel.model_validate(result)
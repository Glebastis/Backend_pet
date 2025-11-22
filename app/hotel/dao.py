from datetime import date
from sqlalchemy import and_, func, insert, or_, select
from app.dao.base import BaseDAO
from app.bookings.dao import BookingDAO
from app.hotel.models import Hotel
from app.database import async_session_maker
from app.rooms.models import Rooms


class HotelDAO(BaseDAO):
    model = Hotel
    
    @classmethod
    async def get_hotels_list_by_region(cls, location: str, date_from: date, date_to: date):
        '''Получение списка отелей с количеством свободных комнат'''
        rooms_left_list = await BookingDAO.rooms_left(date_from, date_to)
        free_room_ids = []
        for room in rooms_left_list:
            if room['rooms_left'] > 0:
                free_room_ids.append(room['id'])
        async with async_session_maker() as session:
            conditions = [cls.model.location.contains(location)]
            if free_room_ids:
                conditions.append(Rooms.id.in_(free_room_ids))
            else:
                # If no free rooms, return empty result
                return []
            
            # First get distinct hotel IDs that match the conditions
            hotel_ids_subquery = select(cls.model.id).distinct().outerjoin(
                Rooms, cls.model.id == Rooms.hotel_id
            ).where(and_(*conditions)).subquery()
            
            # Then fetch the full hotel objects
            all_hotel_region_not_fully_booked = select(cls.model).where(
                cls.model.id.in_(select(hotel_ids_subquery.c.id))
            )
            result = await session.execute(all_hotel_region_not_fully_booked)
            return result.mappings().all()
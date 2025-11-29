from fastapi import APIRouter, Query
from datetime import date
from app.hotel.schemas import SHotel, SRoom
from app.hotel.dao import HotelDAO
from fastapi_cache.decorator import cache
import asyncio


router = APIRouter(
    prefix='/hotels',
    tags=['Отели']
)

@router.get("/{region}", status_code=200)
@cache(expire=20)
async def get_hotels_list_by_region(
                                location: str = Query(...), 
                                date_from: date = Query(...), 
                                date_to: date = Query(...),
                            ) -> list[SHotel]:

    await asyncio.sleep(2)
    return await HotelDAO.get_hotels_list_by_region(location, date_from, date_to)

@router.get("/{hotel_id}/rooms", status_code=200)
async def get_rooms_by_hotel_id(
                            hotel_id: int, 
                            date_from: date = Query(...), 
                            date_to: date = Query(...)
                        ) -> list[SRoom]:
    return await HotelDAO.get_rooms_by_hotel_id(hotel_id, date_from, date_to)

@router.post("/id/{hotel_id}", status_code=200)
async def hotel_by_id(hotel_id: int) -> SHotel:
    return await HotelDAO.get_hotel_by_id(hotel_id)
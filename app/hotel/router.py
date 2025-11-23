from fastapi import APIRouter, Query
from datetime import date
from app.hotel.schemas import SHotel
from app.hotel.dao import HotelDAO


router = APIRouter(
    prefix='/hotels',
    tags=['Отели']
)

@router.get("/{region}", status_code=200)
async def get_hotels_list_by_region(
                                location: str = Query(...), 
                                date_from: date = Query(...), 
                                date_to: date = Query(...),
                            ):# -> list[SHotel]:
    return await HotelDAO.get_hotels_list_by_region(location, date_from, date_to)

@router.get("/{hotel_id}/rooms", status_code=200)
async def get_rooms_by_hotel_id(
                            hotel_id: int, 
                            date_from: date = Query(...), 
                            date_to: date = Query(...)
                        ):
    return await HotelDAO.get_rooms_by_hotel_id(hotel_id, date_from, date_to)
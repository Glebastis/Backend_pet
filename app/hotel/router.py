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
                            ):# -> SHotel:
    return await HotelDAO.get_hotels_list_by_region(location, date_from, date_to)
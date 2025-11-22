from datetime import date
from fastapi import APIRouter, Body, Depends, Request
from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.exceptions import UnauthorizedException
from app.users.dependencies import get_current_user, get_token
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"]
)

@router.get("/bookings", status_code=200)
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    return await BookingDAO.find_all(user_id=user.id)

@router.post("/add_booking", status_code=201)
async def add_booking(
                    user: Users = Depends(get_current_user), 
                    room_id: int = Body(...), 
                    date_from: date = Body(...), 
                    date_to: date = Body(...)
                ) -> SBooking:
    return await BookingDAO.add(
        user=user, 
        room_id=room_id, 
        date_from=date_from, 
        date_to=date_to
    )

@router.get("/{booking_id}")
async def get_booking( booking_id: int) -> SBooking:
    pass
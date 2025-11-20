from fastapi import APIRouter, Depends, Request
from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.exceptions import UnauthorizedException
from app.users.dependencies import get_current_user, get_token

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"]
)

@router.get("")
async def get_bookings(user: dict = Depends(get_current_user)):# -> list[SBooking]:
    return await BookingDAO.find_all(user_id=user.id)

@router.get("/{booking_id}")
async def get_booking(booking_id: int) -> SBooking:
    pass
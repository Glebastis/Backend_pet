from fastapi import APIRouter, Depends, Response

from app.exceptions import UserAlreadyExistsException, UserNotExistsException, InvalidCredentialsException
from app.users.auth import authenticate_user, create_access_token, get_password_hash, verify_password
from app.users.dao import UserDAO
from app.users.schemas import SUserAuth

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"],
)

@router.post("/register", status_code=201)
async def read_users_me(user_data: SUserAuth):
    existing_user = await UserDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UserDAO.add(email=user_data.email, hashed_password=hashed_password)

    return True

@router.post("/login")
async def login(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise InvalidCredentialsException
    access_token = create_access_token({"sub": user.email})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return access_token
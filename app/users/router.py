from fastapi import APIRouter, Depends

from app.exceptions import UserAlreadyExistsException
from app.users.auth import get_password_hash
from app.users.dao import UserDAO
from app.users.schemas import SUserRegister

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"],
)

@router.post("/register", status_code=201)
async def read_users_me(user_data: SUserRegister):
    existing_user = await UserDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UserDAO.add(email=user_data.email, hashed_password=hashed_password)

    return True
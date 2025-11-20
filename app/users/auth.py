from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt

from app.exceptions import InvalidCredentialsException, UserNotExistsException
from app.users.dao import UserDAO
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def authenticate_user(email: str, password: str):
    user = await UserDAO.find_one_or_none(email=email)
    if not user:
        raise UserNotExistsException
    if not verify_password(password, user.hashed_password):
        raise InvalidCredentialsException
    return user
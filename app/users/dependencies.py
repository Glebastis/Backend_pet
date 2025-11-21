from fastapi import Depends, Request
from app.exceptions import UnauthorizedException, TokenExpiredException
from jose import ExpiredSignatureError, jwt, JWTError
from app.config import settings
from app.users.dao import UserDAO


async def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise UnauthorizedException
    return token

async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except ExpiredSignatureError:
        raise TokenExpiredException
    user = await UserDAO.find_one_or_none(email=payload.get("sub"))
    if not user:
        raise UnauthorizedException
    return user
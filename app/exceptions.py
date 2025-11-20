from fastapi import HTTPException, status

class BookingException(HTTPException):
    status_code = 500
    detail = ""
    
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class UserAlreadyExistsException(BookingException):
    status_code=status.HTTP_409_CONFLICT
    detail="Пользователь уже существует"

class UserNotExistsException(BookingException):
    status_code=status.HTTP_404_NOT_FOUND
    detail="Пользователь не найден"

class InvalidCredentialsException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Неверные учетные данные"
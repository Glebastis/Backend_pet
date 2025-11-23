from pydantic import BaseModel

class SHotel(BaseModel):

    id: int
    name: str
    location: str
    services: list[str]
    rooms_quantity: int
    image_id: int

    class Config:
        from_attributes = True

class SRoom(BaseModel):
    id: int
    name: str
    price: int
    services: list[str]
    image_id: int
    rooms_left: int

    class Config:
        from_attributes = True
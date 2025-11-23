from typing import Optional
from app.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column

class Hotel(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    location: Mapped[str] = mapped_column(nullable=False)
    services: Mapped[list[str]] = mapped_column(JSON)
    rooms_quantity: Mapped[int] = mapped_column(nullable=False)
    image_id: Mapped[int]

    def __str__(self):
        return f"Отель {self.name}"

class Rooms(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    price: Mapped[int] = mapped_column(nullable=False)
    services: Mapped[list[str]] = mapped_column(JSON, nullable=True)
    quantity: Mapped[int] = mapped_column(nullable=False)
    image_id: Mapped[int] = mapped_column()

    def __str__(self):
        return f"Номер {self.name}"
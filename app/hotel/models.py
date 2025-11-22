from app.database import Base
from sqlalchemy import Column, Integer, String, JSON
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
from app.database import Base
from sqlalchemy import Column, Integer, Date, ForeignKey, Computed
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date

# class Bookings(Base):
#     __tablename__ = "bookings"

#     id = Column(Integer, primary_key=True)
#     room_id = Column(ForeignKey("rooms.id"), nullable=False)
#     user_id = Column(ForeignKey("users.id"), nullable=False)
#     date_from = Column(Date)
#     date_to = Column(Date)
#     price = Column(Integer)
#     total_cost = Column(Computed("(date_to - date_from) * price"), nullable=False)
#     total_days = Column(Computed("date_to - date_from"), nullable=False)

#     def __str__(self):
#         return f"Бронирование #{self.id}"

class Bookings(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    date_from: Mapped[date] = mapped_column(Date, nullable=False)
    date_to: Mapped[date] = mapped_column(Date, nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    total_cost: Mapped[int] = mapped_column(Computed("(date_to - date_from) * price"), nullable=False)
    total_days: Mapped[int] = mapped_column(Computed("date_to - date_from"), nullable=False)

    def __str__(self):
        return f"Бронирование #{self.id}"
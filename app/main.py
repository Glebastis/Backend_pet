from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from app.bookings.router import router as router_bookings
from app.users.router import router as router_users
from app.hotel.router import router as router_hotel

from app.pages.router import router as router_pages


app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotel)
app.include_router(router_pages)
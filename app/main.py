from fastapi import FastAPI
import uvicorn
from app.bookings.router import router as router_bookings
from app.users.router import router as router_users

app = FastAPI()

app.include_router(router_users)
app.include_router(router_bookings)

@app.get("/")
async def root():
    return {"message": "Привет, мир"}

@app.get("/hotels")
async def get_hotels():
    return "Отель Бридж Резорт 5 звезд"

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
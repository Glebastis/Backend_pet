from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from app.hotel.router import get_hotels_list_by_region

router = APIRouter(
    prefix="/pages",
    tags=["Фронтенд"]
)

templates = Jinja2Templates(directory="app/templates")

@router.get("/hotels")
async def hotels(
            request: Request,
            hotels=Depends(get_hotels_list_by_region)
        ):
    return templates.TemplateResponse(
        "hotels.html", 
        context={"request": request, "hotels": hotels}
        )
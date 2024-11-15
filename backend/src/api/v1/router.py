from fastapi import APIRouter
from .routers.apartment_trade_history import router as apartment_trade_history_router

router = APIRouter(prefix="/api/v1")

router.include_router(apartment_trade_history_router)

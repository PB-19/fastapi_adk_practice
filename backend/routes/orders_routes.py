from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.utils import get_db
from backend.models import Order, DBOrder

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.get("")
async def get_orders(
    db: AsyncSession = Depends(get_db)
):
    pass

@router.get("/{order_id}")
async def get_order_by_id(
    order_id: int,
    db: AsyncSession = Depends(get_db)
):
    pass

@router.post("")
async def create_order(
    order: Order,
    db: AsyncSession = Depends(get_db)
):
    pass
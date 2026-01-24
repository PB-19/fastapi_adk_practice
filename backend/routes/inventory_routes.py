from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.utils import get_db
from backend.models import Inventory, DBInventory

router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.get("")
async def get_inventory(
    db: AsyncSession = Depends(get_db)
):
    pass

@router.get("/low")
async def get_low_inventory(
    db: AsyncSession = Depends(get_db)
):
    pass
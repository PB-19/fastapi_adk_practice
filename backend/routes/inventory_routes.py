from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from backend.utils import get_db
from backend.utils.auth import get_current_user
from backend.models import Inventory, DBInventory, DBUser

router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.get("", response_model=List[Inventory])
async def get_inventory(
    db: AsyncSession = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    sql_query = select(DBInventory)
    result = await db.execute(sql_query)
    inventory = result.scalars().all()
    
    return inventory

@router.get("/low")
async def get_low_inventory(
    min_quantity: int = 3,
    db: AsyncSession = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    sql_query = select(DBInventory).where(DBInventory.quantity < min_quantity)
    result = await db.execute(sql_query)
    inventory = result.scalars().all()
    
    return inventory
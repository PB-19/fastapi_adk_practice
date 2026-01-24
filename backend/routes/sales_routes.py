from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.utils import get_db
from backend.models import Sale, DBSale

router = APIRouter(prefix="/sales", tags=["Sales"])

@router.get("")
async def get_sales(
    db: AsyncSession = Depends(get_db)
):
    pass

@router.get("/{sale_id}")
async def get_sale_by_id(
    sale_id: int,
    db: AsyncSession = Depends(get_db)
):
    pass

@router.post("")
async def create_sale(
    sale: Sale,
    db: AsyncSession = Depends(get_db)
):
    pass
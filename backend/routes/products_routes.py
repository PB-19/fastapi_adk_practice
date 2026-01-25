from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from backend.utils import get_db
from backend.utils.auth import get_current_user
from backend.models import Product, DBProduct, DBUser
from typing import Optional

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("")
async def get_products(
    supplier_id: Optional[int] = Query(None, description="Filter by supplier ID"),
    db: AsyncSession = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    return {
        "message": "User can see products",
    }

@router.get("/{product_id}")
async def get_product_by_id(
    product_id: int,
    db: AsyncSession = Depends(get_db)
):
    pass

@router.post("")
async def create_product(
    product: Product,
    db: AsyncSession = Depends(get_db)
):
    pass

@router.put("")
async def update_product(
    product: Product,
    db: AsyncSession = Depends(get_db)
):
    pass

@router.delete("")
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db)
):
    pass
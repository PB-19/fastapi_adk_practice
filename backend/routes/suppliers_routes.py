from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from backend.utils import get_db
from backend.models import Supplier, DBSupplier
from typing import Optional

router = APIRouter(prefix="/suppliers", tags=["Suppliers"])

@router.get("")
async def get_suppliers(
    location: Optional[str] = Query(None, description="Filter by location"),
    db: AsyncSession = Depends(get_db)
):
    pass

@router.get("/{supplier_id}")
async def get_supplier_by_id(
    supplier_id: int,
    db: AsyncSession = Depends(get_db)
):
    pass

@router.post("")
async def create_supplier(
    supplier: Supplier,
    db: AsyncSession = Depends(get_db)
):
    pass

@router.put("")
async def update_supplier(
    supplier: Supplier,
    db: AsyncSession = Depends(get_db)
):
    pass

@router.delete("")
async def delete_supplier(
    supplier_id: int,
    db: AsyncSession = Depends(get_db)
):
    pass
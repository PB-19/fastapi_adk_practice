from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from backend.utils import get_db
from backend.utils.logger import AppLogger
from backend.utils.auth import get_current_user
from backend.models import Supplier, DBSupplier, DBUser
from backend.models.api_models import (
    GetSuppliersResponse,
    CreateSupplierRequest,
    UpdateSupplierRequest,
)

router = APIRouter(prefix="/suppliers", tags=["Suppliers"])
logger = AppLogger.get_logger(__name__)

@router.get("", response_model=GetSuppliersResponse)
async def get_suppliers(
    location: Optional[str] = Query(None, description="Filter by location"),
    db: AsyncSession = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    logger.info("Retrieving suppliers list...")
    sql_query = select(DBSupplier)
    if location is not None:
        sql_query = sql_query.where(DBSupplier.location == location)

    result = await db.execute(sql_query)
    suppliers = result.scalars().all()
    
    response = GetSuppliersResponse(
        count=len(suppliers),
        suppliers=suppliers
    )
    logger.info(f"Retrieved {len(suppliers)} suppliers.")
    return response

@router.get("/{supplier_id}")
async def get_supplier_by_id(
    supplier_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    logger.info(f"Retrieving supplier with ID {supplier_id}...")
    sql_query = select(DBSupplier).where(DBSupplier.supplier_id == supplier_id)
    result = await db.execute(sql_query)
    supplier = result.scalar_one_or_none()
    if supplier:
        logger.info(f"Supplier with ID {supplier_id} retrieved successfully.")
        return supplier
    else:
        logger.warning(f"Supplier with ID {supplier_id} not found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found",
        )

@router.post("", response_model=Supplier, status_code=status.HTTP_201_CREATED)
async def create_supplier(
    request_body: CreateSupplierRequest,
    db: AsyncSession = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    logger.info("Creating new supplier...")
    db_supplier = DBSupplier(
        supplier_name=request_body.supplier_name,
        location=request_body.location,
        contact_email=request_body.contact_email,
        reliability_score=request_body.reliability_score,
    )
    
    try:
        db.add(db_supplier)
        await db.commit()
        await db.refresh(db_supplier)

        logger.info("Supplier created successfully.")
        return db_supplier

    except Exception as e:
        logger.error(f"Error creating supplier: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

@router.put("")
async def update_supplier(
    request_body: UpdateSupplierRequest,
    db: AsyncSession = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    logger.info(f"Updating supplier with ID {request_body.supplier_id}...")
    sql_query = select(DBSupplier).where(DBSupplier.supplier_id == request_body.supplier_id)
    result = await db.execute(sql_query)
    db_supplier = result.scalar_one_or_none()

    if not db_supplier:
        logger.warning(f"Supplier with ID {request_body.supplier_id} not found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found",
        )
    
    try:
        db_supplier.supplier_name = request_body.supplier_name
        db_supplier.location = request_body.location
        db_supplier.contact_email = request_body.contact_email
        db_supplier.reliability_score = request_body.reliability_score

        await db.commit()
        await db.refresh(db_supplier)

        logger.info(f"Supplier with ID {request_body.supplier_id} updated successfully.")
        return db_supplier
    
    except Exception as e:
        logger.error(f"Error updating supplier with ID {request_body.supplier_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

@router.delete("")
async def delete_supplier(
    supplier_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    logger.info(f"Deleting supplier with ID {supplier_id}...")
    sql_query = select(DBSupplier).where(DBSupplier.supplier_id == supplier_id)
    result = await db.execute(sql_query)
    db_supplier = result.scalar_one_or_none()

    if not db_supplier:
        logger.warning(f"Supplier with ID {supplier_id} not found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found",
        )
    
    try:
        await db.delete(db_supplier)
        await db.commit()

        logger.info(f"Supplier with ID {supplier_id} deleted successfully.")
        return {"message": "Supplier deleted successfully"}
    
    except Exception as e:
        logger.error(f"Error deleting supplier with ID {supplier_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
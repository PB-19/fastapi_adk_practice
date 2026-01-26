from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from backend.utils import get_db
from backend.utils.auth import get_current_user
from backend.models import Product, DBProduct, DBUser
from backend.models.api_models import (
    GetProductsResponse,
    CreateProductRequest,
    UpdateProductRequest,
)

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("", response_model=GetProductsResponse)
async def get_products(
    supplier_id: Optional[int] = Query(None, description="Filter by supplier ID"),
    db: AsyncSession = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
) -> GetProductsResponse:
        
    sql_query = select(DBProduct)
    if supplier_id is not None:
        sql_query = sql_query.where(DBProduct.supplier_id == supplier_id)

    result = await db.execute(sql_query)
    products = result.scalars().all()
    
    response = GetProductsResponse(
        count=len(products),
        products=products
    )
    return response

@router.get("/{product_id}")
async def get_product_by_id(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
) -> Product:
    
    sql_query = select(DBProduct).where(DBProduct.product_id == product_id)
    result = await db.execute(sql_query)
    product = result.scalar_one_or_none()
    if product:
        return product
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

@router.post("", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(
    request_body: CreateProductRequest,
    db: AsyncSession = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    db_product = DBProduct(
        product_name=request_body.product_name,
        category=request_body.category,
        unit_price=request_body.unit_price,
        supplier_id=request_body.supplier_id,
    )
    
    try:
        db.add(db_product)
        await db.commit()
        await db.refresh(db_product)

        return db_product

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

@router.put("")
async def update_product(
    request_body: UpdateProductRequest,
    db: AsyncSession = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    sql_query = select(DBProduct).where(DBProduct.product_id == request_body.product_id)
    result = await db.execute(sql_query)
    db_product = result.scalar_one_or_none()

    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    
    try:
        db_product.product_name = request_body.product_name
        db_product.category = request_body.category
        db_product.unit_price = request_body.unit_price
        db_product.supplier_id = request_body.supplier_id

        await db.commit()
        await db.refresh(db_product)

        return db_product
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

@router.delete("")
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    sql_query = select(DBProduct).where(DBProduct.product_id == product_id)
    result = await db.execute(sql_query)
    db_product = result.scalar_one_or_none()

    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    
    try:
        await db.delete(db_product)
        await db.commit()

        return {"message": "Product deleted successfully"}
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from backend.utils import get_db
from backend.utils.logger import AppLogger
from backend.utils.auth import get_current_user
from backend.models import Sale, DBSale, DBUser, DBProduct, DBInventory
from backend.models.api_models import CreateSaleRequest

router = APIRouter(prefix="/sales", tags=["Sales"])
logger = AppLogger.get_logger(__name__)

async def enrich_sale_items(db, sale_items: list[dict]) -> list[dict]:
    product_ids = {item["product_id"] for item in sale_items}

    result = await db.execute(
        select(DBProduct).where(DBProduct.product_id.in_(product_ids))
    )
    products = result.scalars().all()

    if len(products) != len(product_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid product_id in sale",
        )

    product_map = {
        p.product_id: {
            "supplier_id": p.supplier_id,
            "unit_price": p.unit_price,
        }
        for p in products
    }

    enriched = []
    for item in sale_items:
        unit_price = product_map[item["product_id"]]["unit_price"]
        subtotal = unit_price * item["quantity"]

        enriched.append(
            {
                "product_id": item["product_id"],
                "supplier_id": product_map[item["product_id"]]["supplier_id"],
                "quantity": item["quantity"],
                "unit_price": unit_price,
                "subtotal": subtotal,
            }
        )

    return enriched

async def inventory_is_sufficient(db, enriched_items: list[dict]) -> bool:
    for item in enriched_items:
        result = await db.execute(
            select(DBInventory).where(
                DBInventory.product_id == item["product_id"]
            )
        )
        inventory = result.scalar_one_or_none()

        if not inventory or inventory.quantity < item["quantity"]:
            return False

    return True

@router.get("")
async def get_sales(
    db: AsyncSession = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    logger.info("Retrieving sales list...")
    sql_query = select(DBSale)
    result = await db.execute(sql_query)
    sales = result.scalars().all()

    logger.info(f"Retrieved {len(sales)} sales.")
    return sales

@router.get("/{sale_id}")
async def get_sale_by_id(
    sale_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    logger.info(f"Retrieving sale with ID {sale_id}...")
    sql_query = select(DBSale).where(DBSale.sale_id == sale_id)
    result = await db.execute(sql_query)
    sale = result.scalar_one_or_none()

    if sale:
        logger.info(f"Sale with ID {sale_id} retrieved successfully.")
        return sale
    else:
        logger.warning(f"Sale with ID {sale_id} not found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale not found",
        )

@router.post("")
async def create_sale(
    request_body: CreateSaleRequest,
    db: AsyncSession = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    logger.info("Creating new sale...")
    try:
        enriched_items = await enrich_sale_items(db, request_body.sale_items)

        if not await inventory_is_sufficient(db, enriched_items):
            logger.warning("Insufficient inventory for sale")
            return {
                "message": "Insufficient inventory",
            }

        total_amount = sum(item["subtotal"] for item in enriched_items)

        sale = DBSale(
            sale_details=enriched_items,
            total_amount=total_amount,
            timestamp=datetime.now(),
        )
        db.add(sale)

        await db.flush()

        logger.info(f"Created sale: {sale.sale_id}")

        for item in enriched_items:
            result = await db.execute(
                select(DBInventory).where(
                    DBInventory.product_id == item["product_id"]
                )
            )
            inventory = result.scalar_one()

            inventory.quantity -= item["quantity"]
        logger.info("Updated inventory based on sale items")

        await db.commit()
        await db.refresh(sale)

        return sale
    
    except Exception as e:
        logger.error(f"Error creating sale: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error while making sale:\n{str(e)}",
        )
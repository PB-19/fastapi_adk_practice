from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from backend.utils import get_db
from backend.utils.logger import AppLogger
from backend.utils.auth import get_current_user
from backend.models import Order, DBOrder, DBUser, DBProduct, DBInventory
from backend.models.api_models import CreateOrderRequest

router = APIRouter(prefix="/orders", tags=["Orders"])
logger = AppLogger.get_logger(__name__)

async def enrich_order_items(db, order_items: list[dict]) -> list[dict]:
    product_ids = {item["product_id"] for item in order_items}

    result = await db.execute(
        select(DBProduct).where(DBProduct.product_id.in_(product_ids))
    )
    products = result.scalars().all()

    if len(products) != len(product_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid product_id in order",
        )

    product_map = {
        p.product_id: p.supplier_id for p in products
    }

    enriched_items = []
    for item in order_items:
        subtotal = item["quantity"] * item["unit_price"]
        enriched_items.append(
            {
                "product_id": item["product_id"],
                "supplier_id": product_map[item["product_id"]],
                "quantity": item["quantity"],
                "unit_price": item["unit_price"],
                "subtotal": subtotal,
            }
        )

    return enriched_items

@router.get("")
async def get_orders(
    db: AsyncSession = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    logger.info("Retrieving orders list...")
    sql_query = select(DBOrder)
    result = await db.execute(sql_query)
    orders = result.scalars().all()

    logger.info(f"Retrieved {len(orders)} orders.")
    return orders

@router.get("/{order_id}")
async def get_order_by_id(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    logger.info(f"Retrieving order with ID {order_id}...")
    sql_query = select(DBOrder).where(DBOrder.order_id == order_id)
    result = await db.execute(sql_query)
    order = result.scalar_one_or_none()

    if order:
        logger.info(f"Order with ID {order_id} retrieved successfully.")
        return order
    else:
        logger.warning(f"Order with ID {order_id} not found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

@router.post("")
async def create_order(
    request_body: CreateOrderRequest,
    db: AsyncSession = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    logger.info("Creating new order...")
    try:
        enriched_items = await enrich_order_items(db, request_body.order_items)
        logger.info(f"Enriched order items.")

        total_amount = sum(item["subtotal"] for item in enriched_items)

        order = DBOrder(
            order_details=enriched_items,
            total_amount=total_amount,
            timestamp=datetime.now(),
        )
        db.add(order)

        await db.flush()

        logger.info(f"Created order: {order.order_id}")

        for item in enriched_items:
            result = await db.execute(
                select(DBInventory).where(
                    DBInventory.product_id == item["product_id"]
                )
            )
            inventory = result.scalar_one_or_none()

            if inventory:
                inventory.quantity += item["quantity"]
            else:
                db.add(
                    DBInventory(
                        product_id=item["product_id"],
                        quantity=item["quantity"],
                    )
                )
        logger.info("Updated inventory based on order items")

        await db.commit()
        await db.refresh(order)

        return order
    
    except Exception as e:
        logger.error(f"Error creating order: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error while making order:\n{str(e)}",
        )
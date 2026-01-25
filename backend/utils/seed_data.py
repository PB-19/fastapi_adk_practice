import os
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.models import DBUser, DBSupplier, DBProduct, DBInventory
from backend.utils.auth import hash_password
from backend.utils.logger import AppLogger
from backend.utils.constants import SEED_PRODUCTS_DATA, SEED_SUPPLIERS_DATA, SEED_INVENTORY_DATA
from dotenv import load_dotenv
load_dotenv()

logger = AppLogger.get_logger(__name__)

async def seed_database(db: AsyncSession):
    """Seed the database with initial data if tables are empty"""

    result = await db.execute(select(DBUser).limit(1))
    existing_users = result.scalars().first()

    if existing_users:
        logger.info("USERS table already seeded. Skipping...")
    else:
        raw = str(os.getenv("DEFAULT_PASSWORD")).strip()
        print(f"Password length (chars): {len(raw)}, bytes: {len(raw.encode())}")
        hashed = hash_password(raw)
        print(f"=== HASHED PASSWORD: {hashed} ===")
        user = DBUser(
            username=os.getenv("DEFAULT_USERNAME"),
            password=hashed,
        )
        db.add(user)
        await db.commit()
        logger.info(f"Seeded default user: {user.username}")

    result = await db.execute(select(DBSupplier).limit(1))
    existing_suppliers = result.scalars().first()

    if existing_suppliers:
        logger.info("SUPPLIERS table already seeded. Skipping...")
    else:
        for supplier_data in SEED_SUPPLIERS_DATA:
            supplier = DBSupplier(**supplier_data)
            db.add(supplier)

        await db.commit()
        logger.info(f"Seeded {len(SEED_SUPPLIERS_DATA)} suppliers")

    result = await db.execute(select(DBProduct).limit(1))
    existing_products = result.scalars().first()

    if existing_products:
        logger.info("PRODUCTS table already seeded. Skipping...")
    else:    
        for product_data in SEED_PRODUCTS_DATA:
            product = DBProduct(**product_data)
            db.add(product)

        await db.commit()
        logger.info(f"Seeded {len(SEED_PRODUCTS_DATA)} products")

    result = await db.execute(select(DBInventory).limit(1))
    existing_inventory = result.scalars().first()

    if existing_inventory:
        logger.info("INVENTORY table already seeded. Skipping...")
    else:
        for inventory_item in SEED_INVENTORY_DATA:
            inventory = DBInventory(**inventory_item)
            db.add(inventory)

        await db.commit()
        logger.info(f"Seeded {len(SEED_INVENTORY_DATA)} inventory records")

    logger.info("Database seeding completed successfully!")
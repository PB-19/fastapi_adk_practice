from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.models import DBUser, DBSupplier, DBProduct, DBInventory
from backend.utils.constants import SEED_PRODUCTS_DATA, SEED_SUPPLIERS_DATA, SEED_INVENTORY_DATA

async def seed_database(db: AsyncSession):
    """Seed the database with initial data if tables are empty"""

    # Check if data already exists 
    result = await db.execute(select(DBUser))
    existing_users = result.scalars().first()
    
    if existing_users:
        print("Database already seeded. Skipping...")
        return
    
    print("\nSeeding database...")
    
    for supplier_data in SEED_SUPPLIERS_DATA:
        supplier = DBSupplier(**supplier_data)
        db.add(supplier)
    
    await db.commit()
    print(f"\nSeeded {len(SEED_SUPPLIERS_DATA)} suppliers")
    
    for product_data in SEED_PRODUCTS_DATA:
        product = DBProduct(**product_data)
        db.add(product)
    
    await db.commit()
    print(f"\nSeeded {len(SEED_PRODUCTS_DATA)} products")
    
    for inventory_item in SEED_INVENTORY_DATA:
        inventory = DBInventory(**inventory_item)
        db.add(inventory)
    
    await db.commit()
    print(f"\nSeeded {len(SEED_INVENTORY_DATA)} inventory records")

    print("\nDatabase seeding completed successfully!")
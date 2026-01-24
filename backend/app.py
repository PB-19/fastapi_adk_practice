from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager
from backend.utils import create_tables, close_db, get_db
from backend.routes import (
    login_router,
    products_router,
    suppliers_router,
    inventory_router,
    orders_router,
    sales_router
)
from dotenv import load_dotenv
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup code
    await create_tables()

    yield

    # shutdown code
    await close_db()

app = FastAPI(
    title="Inventory Management API",
    description="Agentic AI backend for managing inventory operations",
    version="0.1.0",
    lifespan=lifespan
)

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(login_router)
api_v1_router.include_router(products_router)
api_v1_router.include_router(suppliers_router)
api_v1_router.include_router(inventory_router)
api_v1_router.include_router(orders_router)
api_v1_router.include_router(sales_router)
app.include_router(api_v1_router)

@app.get("/")
async def root():
    return {"status": "API is running"}

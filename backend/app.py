from fastapi import FastAPI
from contextlib import asynccontextmanager
from backend.utils import create_tables, close_db, get_db
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

@app.get("/")
async def root():
    return {"status": "API is running"}

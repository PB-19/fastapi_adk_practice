import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn

from dotenv import load_dotenv
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup code

    yield

    # shutdown code

app = FastAPI(
    title="Inventory Management API",
    description="Agentic AI backend for managing inventory operations",
    version="0.1.0",
    lifespan=lifespan
)

@app.get("/")
async def root():
    return {"status": "API is running"}

if __name__=="__main__":
    uvicorn.run(app, host=os.getenv("DEFAULT_HOST"), port=os.getenv("DEFAULT_PORT"))
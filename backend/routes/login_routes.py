from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.utils import get_db
from backend.models import User

router = APIRouter(tags=["Authentication"])

@router.post("/login")
async def login():
    pass

@router.post("/register")
async def register():
    pass
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.utils import get_db
from backend.utils.logger import AppLogger
from backend.utils.auth import hash_password, verify_password, create_access_token
from backend.models import DBUser

router = APIRouter(tags=["Authentication"])
logger = AppLogger.get_logger(__name__)

@router.post("/register", status_code=201)
async def register(form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(DBUser).where(DBUser.username == form.username)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    user = DBUser(
        username=form.username,
        password=hash_password(form.password)
    )
    db.add(user)
    await db.commit()

    logger.info(f"New user registered: {form.username}")

    return {"message": "User registered successfully"}

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(DBUser).where(DBUser.username == form.username)
    )
    user = result.scalar_one_or_none()

    if not user or not verify_password(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(user.username)

    logger.info(f"User logged in: {form.username}")

    return {
        "access_token": token,
        "token_type": "bearer"
    }

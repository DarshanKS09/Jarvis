from fastapi import APIRouter, Depends  # depends is a dependency injection system used to provide required objects (like db sessions)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text   #text() lets you run raw SQL safely.
from app.core.database import get_db  #session provider

router = APIRouter()

@router.get("/health/db")  #we can add any name here not dependent on the folder or file
async def check_database(db: AsyncSession = Depends(get_db)):     #creates the session using depends function using get_db()
    try:
        result = await db.execute(text("SELECT 1"))
        return {"status": "Database connected successfully"}
    except Exception as e:
        return {"error": str(e)}
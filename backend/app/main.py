from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes.health import router as health_router
from app.core.database import engine
from app.core.config import settings
import app.models
from app.models.base import Base
from app.routes.tasks import router as tasks_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting Jarvis Backend...")

      # Create tables (MVP only)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("✅ Database tables ensured.")


    yield
    print("🛑 Shutting down Jarvis Backend...")

app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan
)

app.include_router(health_router)
app.include_router(tasks_router)
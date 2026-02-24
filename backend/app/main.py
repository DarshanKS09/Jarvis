from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes.health import router as health_router
from app.core.database import engine
from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting Jarvis Backend...")
    yield
    
    print("🛑 Shutting down Jarvis Backend...")

app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan
)

app.include_router(health_router)
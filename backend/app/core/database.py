from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create async engine
engine = create_async_engine(       # the main powerhouse to create connection with the database
    settings.DATABASE_URL,
    echo=settings.DEBUG,
)

# Create session factory
AsyncSessionLocal = sessionmaker(      #the supervisor who checks and set rules for the sessions created
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Dependency injection for FastAPI
async def get_db():                          # used as the argument in depend in further routing to get sessions for that request
    async with AsyncSessionLocal() as session:
        yield session
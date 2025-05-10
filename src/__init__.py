from fastapi import FastAPI
from src.users.routes import users_router

async def lifespan(app: FastAPI):
    """
    Lifespan function to initialize the database.
    """
    from src.db.main import init_db
    print("Starting up...")
    await init_db()
    yield
    print("Shutting down...")

app = FastAPI(
    title="FastAPI User Management",
    description="A simple user management API built with FastAPI.",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
)
app.include_router(prefix="/api/v1/users", tags=["Users"], router=users_router)
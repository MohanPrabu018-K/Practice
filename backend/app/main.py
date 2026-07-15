"""FastAPI application factory with all routers."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.models import *
from app.routers import auth, core, admin

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

def create_app() -> FastAPI:
    app = FastAPI(title="Movie Ticket Booking API", description="Production-grade movie ticket booking system", version="2.0.0", lifespan=lifespan, docs_url="/docs", redoc_url="/redoc")
    app.add_middleware(CORSMiddleware, allow_origins=settings.CORS_ORIGINS, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
    app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
    app.include_router(core.router, tags=["Core"])
    app.include_router(admin.router, tags=["Admin"])
    return app

app = create_app()

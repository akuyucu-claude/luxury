from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
from app.routers import brands, news, financial, analytics
from app.services.scheduler import start_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    start_scheduler()
    yield


app = FastAPI(
    title="Luxury Brand Monitor",
    description="API for monitoring luxury brand news, financials, and sentiment",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(brands.router, prefix="/api")
app.include_router(news.router, prefix="/api")
app.include_router(financial.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Luxury Brand Monitor API", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}

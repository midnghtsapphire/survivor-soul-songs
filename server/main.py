"""FastAPI application for Survivor Soul Songs."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from server.config import settings
from server.database import init_db
from server.routes import auth, billing

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"🚀 Starting {settings.APP_NAME}")
    print(f"📍 Stripe Mode: {settings.STRIPE_MODE}")
    init_db()
    yield
    print(f"👋 Shutting down {settings.APP_NAME}")

app = FastAPI(
    title="Survivor Soul Songs API",
    description="Survivor Soul Songs backend API with auth, billing, and features",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "stripe_mode": settings.STRIPE_MODE
    }

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(billing.router, prefix="/api/billing", tags=["Billing"])

if __name__ == "__main__":
    uvicorn.run("server.main:app", host="0.0.0.0", port=8003, reload=True)

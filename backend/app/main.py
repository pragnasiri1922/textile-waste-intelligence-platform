import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import models
from database import engine, Base
from routers import auth_router, inventory_router, analytics_router, upload_router, classification_router

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Textile Waste Intelligence Platform API",
    description="Intelligent platform for tracking, analyzing, and optimizing textile waste operations.",
    version="2.0.0"
)

# Configure CORS - allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth_router.router)
app.include_router(inventory_router.router)
app.include_router(analytics_router.router)
app.include_router(upload_router.router)
app.include_router(classification_router.router)

# Resolve frontend directory path relative to project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"

# Mount frontend static files
if FRONTEND_DIR.exists():
    app.mount("/app", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Textile Waste Intelligence Platform API",
        "version": "2.0.0",
        "docs": "/docs",
        "frontend": "/app",
    }
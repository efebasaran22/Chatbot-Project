"""Main FastAPI application."""
#
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.core.config import settings
from app.core.logging import setup_logging
from app.api.v1.router import api_router

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events.
    
    Startup: Initialize services, load models, etc.
    Shutdown: Cleanup resources.
    """
    # Startup
    logger.info("🚀 Starting MSKÜ ChatBot API...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"LLM Provider: {settings.LLM_PROVIDER}")
    
    # TODO: Initialize services here
    # - Load embedding model
    # - Initialize ChromaDB
    # - Setup LLM client
    
    logger.info("✅ Application startup complete!")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down MSKÜ ChatBot API...")
    
    # TODO: Cleanup resources
    # - Close database connections
    # - Save cache
    # - Cleanup temporary files
    
    logger.info("✅ Application shutdown complete!")


# Create FastAPI application
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    lifespan=lifespan,
    docs_url=f"{settings.API_V1_PREFIX}/docs",
    redoc_url=f"{settings.API_V1_PREFIX}/redoc",
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_path = Path(__file__).parent / "static"
static_path.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")


@app.get("/", include_in_schema=False)
async def root():
    """Serve QA management interface from root."""
    return FileResponse(str(static_path / "qa_management.html"))


@app.get("/qa-management", include_in_schema=False)
async def qa_management():
    """Serve QA management interface."""
    return FileResponse(str(static_path / "qa_management.html"))


# Include API v1 router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )

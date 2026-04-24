"""Health check endpoint."""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict

router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    version: str
    environment: str


@router.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check() -> HealthResponse:
    """
    Health check endpoint.
    
    Returns the service status and version information.
    """
    from app.core.config import settings
    from app import __version__
    
    return HealthResponse(
        status="healthy",
        version=__version__,
        environment=settings.ENVIRONMENT
    )

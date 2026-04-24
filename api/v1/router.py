"""API v1 router configuration."""
from fastapi import APIRouter
from app.api.v1.endpoints import health, chat, qa

# Create main v1 router
api_router = APIRouter()

# Include health check (no prefix, at root level)
api_router.include_router(health.router, tags=["Health"])

# Include chat endpoints
api_router.include_router(
    chat.router,
    prefix="/chat",
    tags=["Chat"]
)

# Include QA management endpoints
api_router.include_router(qa.router)

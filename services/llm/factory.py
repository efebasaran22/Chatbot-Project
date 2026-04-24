"""LLM factory to choose provider based on settings."""
from __future__ import annotations
import logging
from typing import Optional

from app.core.config import settings
from .base import LLMService
from .groq_service import GroqLLMService

logger = logging.getLogger(__name__)


def get_llm_service() -> Optional[LLMService]:
    provider = settings.LLM_PROVIDER.lower()
    try:
        if provider == "groq":
            return GroqLLMService()
        elif provider == "ollama":
            logger.warning("Ollama provider not yet implemented. Falling back to None.")
            return None
        else:
            logger.warning("Unknown LLM provider '%s'", provider)
            return None
    except Exception as e:
        logger.error("LLM service initialization failed: %s", e)
        return None

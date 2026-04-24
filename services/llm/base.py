"""Abstract base for LLM services."""
from __future__ import annotations
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class LLMResult:
    content: str
    model_used: Optional[str] = None
    tokens_used: Optional[int] = None
    raw: Optional[Dict[str, Any]] = None


class LLMService:
    """Base interface for LLM providers."""

    def generate(
        self,
        question: str,
        *,
        system_prompt: Optional[str] = None,
        max_tokens: int = 500,
        temperature: float = 0.3,
    ) -> LLMResult:
        raise NotImplementedError

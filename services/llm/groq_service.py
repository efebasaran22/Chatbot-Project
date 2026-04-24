"""Groq LLM service implementation."""
from __future__ import annotations
from typing import Optional
import logging

from groq import Groq
from app.core.config import settings
from .base import LLMService, LLMResult

logger = logging.getLogger(__name__)


class GroqLLMService(LLMService):
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.GROQ_API_KEY
        self.model = model or settings.GROQ_MODEL
        if not self.api_key:
            raise ValueError("GROQ_API_KEY is not set")
        self.client = Groq(api_key=self.api_key)

    def generate(
        self,
        question: str,
        *,
        system_prompt: Optional[str] = None,
        max_tokens: int = 500,
        temperature: float = 0.3,
    ) -> LLMResult:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": question})

        logger.info("Calling Groq LLM: %s", self.model)
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        content = resp.choices[0].message.content
        usage = getattr(resp, "usage", None)
        tokens_used = None
        if usage:
            tokens_used = getattr(usage, "total_tokens", None)
        return LLMResult(content=content, model_used=self.model, tokens_used=tokens_used, raw=resp.__dict__)

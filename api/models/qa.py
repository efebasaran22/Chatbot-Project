"""Pydantic models for QA (Question-Answer) management."""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class QACreate(BaseModel):
    """Model for creating a new QA pair."""
    question: str = Field(
        ..., 
        description="Soru metni",
        min_length=3,
        max_length=1000
    )
    answer: str = Field(
        ..., 
        description="Cevap metni",
        min_length=1,
        max_length=5000
    )
    category: Optional[str] = Field(
        None,
        description="Kategori (opsiyonel)",
        max_length=100
    )


class QAUpdate(BaseModel):
    """Model for updating an existing QA pair."""
    question: Optional[str] = Field(
        None,
        description="Soru metni",
        min_length=3,
        max_length=1000
    )
    answer: Optional[str] = Field(
        None,
        description="Cevap metni",
        min_length=1,
        max_length=5000
    )
    category: Optional[str] = Field(
        None,
        description="Kategori",
        max_length=100
    )


class QAResponse(BaseModel):
    """Model for QA pair response."""
    id: str = Field(..., description="Benzersiz ID")
    question: str = Field(..., description="Soru metni")
    answer: str = Field(..., description="Cevap metni")
    category: Optional[str] = Field(None, description="Kategori")
    created_at: datetime = Field(..., description="Oluşturulma tarihi")
    updated_at: Optional[datetime] = Field(None, description="Güncellenme tarihi")


class QAListResponse(BaseModel):
    """Model for list of QA pairs."""
    total: int = Field(..., description="Toplam kayıt sayısı")
    items: list[QAResponse] = Field(..., description="QA çiftleri listesi")


class MessageResponse(BaseModel):
    """Generic message response."""
    message: str = Field(..., description="Mesaj")

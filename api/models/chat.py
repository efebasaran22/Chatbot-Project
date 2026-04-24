"""Pydantic models for chat requests and responses."""
from typing import List, Optional
from pydantic import BaseModel, Field


class Source(BaseModel):
    """Document source information."""
    document_name: str = Field(..., description="Doküman adı")
    page_number: Optional[int] = Field(None, description="Sayfa numarası")
    relevance_score: float = Field(..., description="İlgililik puanı (0-1)")
    excerpt: Optional[str] = Field(None, description="İlgili metin parçası")


class ChatRequest(BaseModel):
    """Chat request model."""
    question: str = Field(
        ..., 
        description="Kullanıcının sorusu",
        min_length=3,
        max_length=500
    )
    conversation_id: Optional[str] = Field(
        None, 
        description="Sohbet ID'si (opsiyonel)"
    )
    include_sources: bool = Field(
        True, 
        description="Kaynak dokümanları dahil et"
    )
    max_tokens: Optional[int] = Field(
        500, 
        description="Maksimum token sayısı",
        ge=50,
        le=2000
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "MSKÜ hangi yılda kuruldu?",
                "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
                "include_sources": True,
                "max_tokens": 500
            }
        }


class ChatResponseData(BaseModel):
    """Chat response data model."""
    answer: str = Field(..., description="LLM'den gelen yanıt")
    conversation_id: str = Field(..., description="Sohbet ID'si")
    sources: List[Source] = Field(default_factory=list, description="Kaynak dokümanlar")
    confidence_score: Optional[float] = Field(None, description="Güven puanı (0-1)")
    processing_time_ms: Optional[int] = Field(None, description="İşlem süresi (ms)")
    model_used: Optional[str] = Field(None, description="Kullanılan model")
    tokens_used: Optional[int] = Field(None, description="Kullanılan token sayısı")


class ChatResponse(BaseModel):
    """Chat response model."""
    success: bool = Field(..., description="İşlem başarılı mı?")
    data: Optional[ChatResponseData] = Field(None, description="Yanıt verisi")
    timestamp: str = Field(..., description="Zaman damgası")


class ErrorDetail(BaseModel):
    """Error detail model."""
    code: str = Field(..., description="Hata kodu")
    message: str = Field(..., description="Hata mesajı")
    details: Optional[dict] = Field(None, description="Ek detaylar")


class ErrorResponse(BaseModel):
    """Error response model."""
    success: bool = Field(False, description="İşlem başarısız")
    error: ErrorDetail = Field(..., description="Hata detayları")
    timestamp: str = Field(..., description="Zaman damgası")

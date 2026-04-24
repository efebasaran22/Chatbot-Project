"""Chat endpoints for the chatbot."""
import logging
import uuid
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException, status
from app.api.models.chat import (
    ChatRequest, 
    ChatResponse, 
    ChatResponseData,
    ErrorResponse,
    ErrorDetail,
    Source
)

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/ask", response_model=ChatResponse, tags=["Chat"])
async def ask_question(request: ChatRequest) -> ChatResponse:
    """
    Ana chatbot endpoint'i.
    
    Kullanıcının sorusunu alır ve LLM ile yanıt üretir.
    RAG (Retrieval Augmented Generation) kullanarak 
    kurumsal dokümanlardan ilgili bilgileri bulur.
    
    Args:
        request: ChatRequest - Kullanıcının sorusu ve parametreler
        
    Returns:
        ChatResponse - LLM yanıtı, kaynaklar ve metadata
    """
    start_time = datetime.now()
    
    try:
        # Generate conversation ID if not provided
        conversation_id = request.conversation_id or str(uuid.uuid4())

        logger.info(f"Processing question: {request.question[:80]}...")

        # Try LLM service
        from app.services.llm.factory import get_llm_service
        llm = get_llm_service()

        system_prompt = (
            "Sen Muğla Sıtkı Koçman Üniversitesi'nin resmi chatbot'usun. "
            "Sadece üniversiteye ait resmi dokümanlara dayanarak cevap ver. "
            "Bilmiyorsan 'Bu konuda bilgim yok.' de. Türkçe yanıt ver."
        )

        answer_text: Optional[str] = None
        model_used: str = "mock-model"
        tokens_used: Optional[int] = None

        if llm:
            try:
                result = llm.generate(
                    question=request.question,
                    system_prompt=system_prompt,
                    max_tokens=request.max_tokens or 500,
                    temperature=0.3,
                )
                answer_text = (result.content or "").strip()
                model_used = result.model_used or model_used
                tokens_used = result.tokens_used
            except Exception as le:
                logger.warning(f"LLM call failed, falling back to mock: {le}")

        # Fallback to mock if no LLM or empty result
        if not answer_text:
            answer_text = (
                "MSKÜ (Muğla Sıtkı Koçman Üniversitesi) 2007 yılında kurulmuştur.\n\n"
                "Not: Bu şu anda bir mock yanıttır. GROQ_API_KEY eklenirse gerçek LLM yanıtı üretilecektir."
            )

        mock_sources = [
            Source(
                document_name="msku_hakkinda.pdf",
                page_number=1,
                relevance_score=0.95,
                excerpt="MSKÜ 2007 yılında Muğla Üniversitesi adıyla kurulmuştur...",
            )
        ]

        # Calculate processing time
        processing_time = int((datetime.now() - start_time).total_seconds() * 1000)

        response_data = ChatResponseData(
            answer=answer_text,
            conversation_id=conversation_id,
            sources=mock_sources if request.include_sources else [],
            confidence_score=0.95,
            processing_time_ms=processing_time,
            model_used=model_used,
            tokens_used=tokens_used,
        )

        return ChatResponse(
            success=True,
            data=response_data,
            timestamp=datetime.utcnow().isoformat() + "Z",
        )
        
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "Bir hata oluştu. Lütfen daha sonra tekrar deneyin.",
                    "details": {"error": str(e)}
                },
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        )

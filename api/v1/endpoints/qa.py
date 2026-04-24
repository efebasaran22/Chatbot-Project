"""QA (Question-Answer) management endpoints."""
import logging
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query

from app.api.models.qa import (
    QACreate, 
    QAUpdate, 
    QAResponse, 
    QAListResponse,
    MessageResponse
)
from app.services.qa_storage import qa_storage

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/qa", tags=["QA Management"])


@router.post("/", response_model=QAResponse, status_code=201)
async def create_qa_pair(qa_data: QACreate):
    """Create a new question-answer pair.
    
    Args:
        qa_data: QA pair data
        
    Returns:
        Created QA pair with ID and timestamps
    """
    try:
        logger.info(f"Creating new QA pair: {qa_data.question[:50]}...")
        
        qa_pair = qa_storage.create_qa(
            question=qa_data.question,
            answer=qa_data.answer,
            category=qa_data.category
        )
        
        logger.info(f"✅ QA pair created with ID: {qa_pair['id']}")
        return qa_pair
        
    except Exception as e:
        logger.error(f"❌ Error creating QA pair: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating QA pair: {str(e)}")


@router.get("/", response_model=QAListResponse)
async def get_all_qa_pairs(
    category: Optional[str] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(None, description="Search in questions and answers")
):
    """Get all QA pairs with optional filtering.
    
    Args:
        category: Optional category filter
        search: Optional search query
        
    Returns:
        List of QA pairs with total count
    """
    try:
        if search:
            logger.info(f"Searching QA pairs with query: {search}")
            qa_pairs = qa_storage.search_qa(search)
        else:
            logger.info(f"Fetching all QA pairs (category: {category})")
            qa_pairs = qa_storage.get_all_qa(category=category)
        
        return {
            "total": len(qa_pairs),
            "items": qa_pairs
        }
        
    except Exception as e:
        logger.error(f"❌ Error fetching QA pairs: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching QA pairs: {str(e)}")


@router.get("/{qa_id}", response_model=QAResponse)
async def get_qa_pair(qa_id: str):
    """Get a specific QA pair by ID.
    
    Args:
        qa_id: QA pair ID
        
    Returns:
        QA pair data
    """
    try:
        logger.info(f"Fetching QA pair: {qa_id}")
        
        qa_pair = qa_storage.get_qa_by_id(qa_id)
        
        if not qa_pair:
            raise HTTPException(status_code=404, detail="QA pair not found")
        
        return qa_pair
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error fetching QA pair: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching QA pair: {str(e)}")


@router.put("/{qa_id}", response_model=QAResponse)
async def update_qa_pair(qa_id: str, qa_data: QAUpdate):
    """Update an existing QA pair.
    
    Args:
        qa_id: QA pair ID
        qa_data: Updated QA data
        
    Returns:
        Updated QA pair
    """
    try:
        logger.info(f"Updating QA pair: {qa_id}")
        
        qa_pair = qa_storage.update_qa(
            qa_id=qa_id,
            question=qa_data.question,
            answer=qa_data.answer,
            category=qa_data.category
        )
        
        if not qa_pair:
            raise HTTPException(status_code=404, detail="QA pair not found")
        
        logger.info(f"✅ QA pair updated: {qa_id}")
        return qa_pair
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error updating QA pair: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating QA pair: {str(e)}")


@router.delete("/{qa_id}", response_model=MessageResponse)
async def delete_qa_pair(qa_id: str):
    """Delete a QA pair.
    
    Args:
        qa_id: QA pair ID
        
    Returns:
        Success message
    """
    try:
        logger.info(f"Deleting QA pair: {qa_id}")
        
        success = qa_storage.delete_qa(qa_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="QA pair not found")
        
        logger.info(f"✅ QA pair deleted: {qa_id}")
        return {"message": "QA pair deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error deleting QA pair: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting QA pair: {str(e)}")

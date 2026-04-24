"""QA (Question-Answer) storage service."""
import json
import os
from datetime import datetime
from typing import List, Optional
from pathlib import Path
import uuid


class QAStorageService:
    """Service for managing QA pairs storage."""
    
    def __init__(self, storage_path: str = "./app/data/qa_data.json"):
        """Initialize QA storage service.
        
        Args:
            storage_path: Path to JSON storage file
        """
        self.storage_path = Path(storage_path)
        self._ensure_storage_exists()
    
    def _ensure_storage_exists(self):
        """Ensure storage directory and file exist."""
        # Create directory if it doesn't exist
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create file with empty list if it doesn't exist
        if not self.storage_path.exists():
            self._save_data([])
    
    def _load_data(self) -> List[dict]:
        """Load QA data from JSON file."""
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _save_data(self, data: List[dict]):
        """Save QA data to JSON file."""
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)
    
    def create_qa(self, question: str, answer: str, category: Optional[str] = None) -> dict:
        """Create a new QA pair.
        
        Args:
            question: Question text
            answer: Answer text
            category: Optional category
            
        Returns:
            Created QA pair with ID and timestamps
        """
        data = self._load_data()
        
        qa_pair = {
            "id": str(uuid.uuid4()),
            "question": question,
            "answer": answer,
            "category": category,
            "created_at": datetime.now().isoformat(),
            "updated_at": None
        }
        
        data.append(qa_pair)
        self._save_data(data)
        
        return qa_pair
    
    def get_all_qa(self, category: Optional[str] = None) -> List[dict]:
        """Get all QA pairs, optionally filtered by category.
        
        Args:
            category: Optional category filter
            
        Returns:
            List of QA pairs
        """
        data = self._load_data()
        
        if category:
            data = [qa for qa in data if qa.get("category") == category]
        
        return data
    
    def get_qa_by_id(self, qa_id: str) -> Optional[dict]:
        """Get a specific QA pair by ID.
        
        Args:
            qa_id: QA pair ID
            
        Returns:
            QA pair if found, None otherwise
        """
        data = self._load_data()
        
        for qa in data:
            if qa["id"] == qa_id:
                return qa
        
        return None
    
    def update_qa(self, qa_id: str, question: Optional[str] = None, 
                  answer: Optional[str] = None, category: Optional[str] = None) -> Optional[dict]:
        """Update a QA pair.
        
        Args:
            qa_id: QA pair ID
            question: New question text (optional)
            answer: New answer text (optional)
            category: New category (optional)
            
        Returns:
            Updated QA pair if found, None otherwise
        """
        data = self._load_data()
        
        for qa in data:
            if qa["id"] == qa_id:
                if question is not None:
                    qa["question"] = question
                if answer is not None:
                    qa["answer"] = answer
                if category is not None:
                    qa["category"] = category
                qa["updated_at"] = datetime.now().isoformat()
                
                self._save_data(data)
                return qa
        
        return None
    
    def delete_qa(self, qa_id: str) -> bool:
        """Delete a QA pair.
        
        Args:
            qa_id: QA pair ID
            
        Returns:
            True if deleted, False if not found
        """
        data = self._load_data()
        original_length = len(data)
        
        data = [qa for qa in data if qa["id"] != qa_id]
        
        if len(data) < original_length:
            self._save_data(data)
            return True
        
        return False
    
    def search_qa(self, query: str) -> List[dict]:
        """Search QA pairs by keyword.
        
        Args:
            query: Search query
            
        Returns:
            List of matching QA pairs
        """
        data = self._load_data()
        query_lower = query.lower()
        
        results = []
        for qa in data:
            if (query_lower in qa["question"].lower() or 
                query_lower in qa["answer"].lower() or
                (qa.get("category") and query_lower in qa["category"].lower())):
                results.append(qa)
        
        return results


# Create singleton instance
qa_storage = QAStorageService()

"""Custom exceptions for the application."""


class MSKUChatBotException(Exception):
    """Base exception for MSKÜ ChatBot."""
    pass


class LLMServiceError(MSKUChatBotException):
    """Raised when LLM service encounters an error."""
    pass


class EmbeddingServiceError(MSKUChatBotException):
    """Raised when embedding service encounters an error."""
    pass


class VectorDBError(MSKUChatBotException):
    """Raised when vector database encounters an error."""
    pass


class DocumentProcessingError(MSKUChatBotException):
    """Raised when document processing fails."""
    pass


class ValidationError(MSKUChatBotException):
    """Raised when input validation fails."""
    pass


class RateLimitExceeded(MSKUChatBotException):
    """Raised when rate limit is exceeded."""
    pass

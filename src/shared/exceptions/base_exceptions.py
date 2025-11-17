# =============================================================================
# src/shared/exceptions/base_exceptions.py
# =============================================================================
"""Base Exceptions for the application"""


class DomainException(Exception):
    """Base exception for domain layer"""
    
    def __init__(self, message: str, details: dict = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)
    
    def __str__(self):
        if self.details:
            return f"{self.message} | Details: {self.details}"
        return self.message


class ValidationException(DomainException):
    """Raised when validation fails"""
    pass


class EntityNotFoundException(DomainException):
    """Raised when entity is not found"""
    pass


class InvalidOperationException(DomainException):
    """Raised when operation is invalid"""
    pass


class InfrastructureException(Exception):
    """Base exception for infrastructure layer"""
    
    def __init__(self, message: str, cause: Exception = None):
        self.message = message
        self.cause = cause
        super().__init__(self.message)


class ParsingException(InfrastructureException):
    """Raised when parsing fails"""
    pass


class FileSystemException(InfrastructureException):
    """Raised when file system operation fails"""
    pass


class RepositoryException(InfrastructureException):
    """Raised when repository operation fails"""
    pass


class ApplicationException(Exception):
    """Base exception for application layer"""
    
    def __init__(self, message: str, recoverable: bool = False):
        self.message = message
        self.recoverable = recoverable
        super().__init__(self.message)


class UseCaseException(ApplicationException):
    """Raised when use case execution fails"""
    pass


class ServiceException(ApplicationException):
    """Raised when service operation fails"""
    pass
# =============================================================================
# src/shared/exceptions/__init__.py
# =============================================================================
"""Exceptions Package"""

from .base_exceptions import (
    DomainException,
    ValidationException,
    EntityNotFoundException,
    InvalidOperationException,
    InfrastructureException,
    ParsingException,
    FileSystemException,
    RepositoryException,
    ApplicationException,
    UseCaseException,
    ServiceException
)

from .parsing_exceptions import (
    SyntaxParsingException,
    ImportParsingException,
    MockParsingException,
    TestStructureParsingException,
    UnsupportedFileTypeException,
    FileEncodingException
)

from .validation_exceptions import (
    ConfigValidationException,
    SchemaValidationException,
    FileValidationException,
    PathValidationException,
    ValueRangeException,
    RequiredFieldException,
    TypeValidationException
)

__all__ = [
    # Base exceptions
    'DomainException',
    'ValidationException',
    'EntityNotFoundException',
    'InvalidOperationException',
    'InfrastructureException',
    'ParsingException',
    'FileSystemException',
    'RepositoryException',
    'ApplicationException',
    'UseCaseException',
    'ServiceException',
    # Parsing exceptions
    'SyntaxParsingException',
    'ImportParsingException',
    'MockParsingException',
    'TestStructureParsingException',
    'UnsupportedFileTypeException',
    'FileEncodingException',
    # Validation exceptions
    'ConfigValidationException',
    'SchemaValidationException',
    'FileValidationException',
    'PathValidationException',
    'ValueRangeException',
    'RequiredFieldException',
    'TypeValidationException'
]
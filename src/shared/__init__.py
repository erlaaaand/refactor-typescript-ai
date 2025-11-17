# =============================================================================
# src/shared/__init__.py
# =============================================================================
"""
Shared Kernel Package

This package contains code that is shared across all layers.
It includes exceptions, validators, and utility functions.

Components:
- Exceptions: Custom exception classes for the entire application
- Validators: Validation logic used across layers
- Utils: Utility functions (file, string, math operations)
"""

from .exceptions import (
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
    ServiceException,
    SyntaxParsingException,
    ImportParsingException,
    MockParsingException,
    TestStructureParsingException,
    UnsupportedFileTypeException,
    FileEncodingException,
    ConfigValidationException,
    SchemaValidationException,
    FileValidationException,
    PathValidationException,
    ValueRangeException,
    RequiredFieldException,
    TypeValidationException
)

from .validators import (
    FileValidator,
    PlanValidator
)

from .utils import (
    FileUtils,
    StringUtils,
    MathUtils
)

__all__ = [
    # Base Exceptions
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
    # Parsing Exceptions
    'SyntaxParsingException',
    'ImportParsingException',
    'MockParsingException',
    'TestStructureParsingException',
    'UnsupportedFileTypeException',
    'FileEncodingException',
    # Validation Exceptions
    'ConfigValidationException',
    'SchemaValidationException',
    'FileValidationException',
    'PathValidationException',
    'ValueRangeException',
    'RequiredFieldException',
    'TypeValidationException',
    # Validators
    'FileValidator',
    'PlanValidator',
    # Utils
    'FileUtils',
    'StringUtils',
    'MathUtils'
]

__version__ = '2.1.0'
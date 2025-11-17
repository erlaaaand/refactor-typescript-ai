# =============================================================================
# src/domain/__init__.py
# =============================================================================
"""
Domain Layer Package

This is the heart of the application containing pure business logic.
The domain layer has no dependencies on external frameworks or libraries.

Components:
- Entities: Business objects with identity and behavior
- Value Objects: Immutable objects defined by their attributes
- Repositories: Interfaces for data access (implementations in infrastructure)
"""

from .entities import (
    TestFile,
    Pattern,
    PatternType,
    PatternFrequency,
    RefactorPlan,
    RefactorAction,
    PlanStatus,
    FileOperation
)

from .value_objects import (
    Complexity,
    ComplexityLevel,
    QualityScore,
    QualityLevel,
    FileMetadata
)

from .repositories import (
    TestFileRepository,
    PatternRepository
)

__all__ = [
    # Entities
    'TestFile',
    'Pattern',
    'PatternType',
    'PatternFrequency',
    'RefactorPlan',
    'RefactorAction',
    'PlanStatus',
    'FileOperation',
    # Value Objects
    'Complexity',
    'ComplexityLevel',
    'QualityScore',
    'QualityLevel',
    'FileMetadata',
    # Repositories
    'TestFileRepository',
    'PatternRepository'
]

__version__ = '2.1.0'
__author__ = 'Test Refactor AI Team'
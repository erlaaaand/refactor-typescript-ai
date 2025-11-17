# =============================================================================
# src/application/__init__.py
# =============================================================================
"""
Application Layer Package

This layer orchestrates the flow of data to and from the domain layer.
It contains use cases (application-specific business rules) and services.

Components:
- Use Cases: Application-specific business logic workflows
- Services: Orchestration services that coordinate multiple operations
- DTOs: Data Transfer Objects for moving data between layers
"""

from .use_cases import (
    AnalyzeTestFilesUseCase,
    AnalyzeTestFilesRequest,
    GenerateRefactorPlanUseCase,
    GenerateRefactorPlanRequest,
    ExecuteRefactoringUseCase,
    ExecuteRefactoringRequest
)

from .services import (
    AnalysisService,
    PlanningService,
    ExecutionService
)

from .dto import (
    AnalysisResult,
    PlanGenerationResult,
    ExecutionResult
)

__all__ = [
    # Use Cases
    'AnalyzeTestFilesUseCase',
    'AnalyzeTestFilesRequest',
    'GenerateRefactorPlanUseCase',
    'GenerateRefactorPlanRequest',
    'ExecuteRefactoringUseCase',
    'ExecuteRefactoringRequest',
    # Services
    'AnalysisService',
    'PlanningService',
    'ExecutionService',
    # DTOs
    'AnalysisResult',
    'PlanGenerationResult',
    'ExecutionResult'
]

__version__ = '2.1.0'
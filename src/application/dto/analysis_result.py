# =============================================================================
# src/application/dto/analysis_result.py
# =============================================================================
"""Data Transfer Objects for Application Layer"""

from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime


@dataclass
class AnalysisResult:
    """Result of test file analysis"""
    total_files: int
    analyzed_files: int
    candidates_for_refactoring: int
    statistics: Dict
    execution_time: float
    timestamp: datetime


@dataclass
class PlanGenerationResult:
    """Result of refactoring plan generation"""
    total_plans: int
    split_by_category: int
    split_by_concern: int
    extract_shared: int
    keep_as_is: int
    avg_confidence: float
    timestamp: datetime


@dataclass
class ExecutionResult:
    """Result of refactoring execution"""
    total_executed: int
    successful: int
    failed: int
    files_created: int
    execution_time: float
    timestamp: datetime
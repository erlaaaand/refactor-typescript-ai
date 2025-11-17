# =============================================================================
# src/application/use_cases/generate_refactor_plan.py
# =============================================================================
"""Use Case: Generate Refactoring Plans"""

from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional

from ..services.planning_service import PlanningService
from ..dto.analysis_result import PlanGenerationResult
from ...domain.entities.test_file import TestFile
from ...domain.entities.refactor_plan import RefactorPlan


@dataclass
class GenerateRefactorPlanRequest:
    """Request for generating refactoring plans"""
    test_files: Optional[List[TestFile]] = None
    max_files: Optional[int] = None
    target_file: Optional[Path] = None
    verbose: bool = False


class GenerateRefactorPlanUseCase:
    """Use case for generating refactoring plans"""
    
    def __init__(self, planning_service: PlanningService):
        self.planning_service = planning_service
    
    def execute(self, request: GenerateRefactorPlanRequest) -> tuple[List[RefactorPlan], PlanGenerationResult]:
        """Execute the plan generation use case"""
        
        if request.verbose:
            print("🎯 Generating refactoring plans...")
            if request.max_files:
                print(f"   Max files: {request.max_files}")
            if request.target_file:
                print(f"   Target file: {request.target_file}")
        
        # Get test files to analyze
        test_files = request.test_files
        if test_files is None:
            test_files = self.planning_service.repository.find_needing_refactoring()
        
        # Filter by target file if specified
        if request.target_file:
            test_files = [
                tf for tf in test_files 
                if tf.metadata.path == request.target_file
            ]
        
        # Limit number of files if specified
        if request.max_files:
            test_files = test_files[:request.max_files]
        
        if request.verbose:
            print(f"   Files to analyze: {len(test_files)}")
        
        # Generate plans
        plans = self.planning_service.generate_plans(test_files)
        
        # Generate summary
        summary = self.planning_service.generate_summary(plans)
        
        if request.verbose:
            print(f"\n✅ Plan generation complete!")
            print(f"   Total plans: {summary.total_plans}")
            print(f"   Avg confidence: {summary.avg_confidence:.2%}")
        
        return plans, summary
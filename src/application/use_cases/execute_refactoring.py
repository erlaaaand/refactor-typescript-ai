# =============================================================================
# src/application/use_cases/execute_refactoring.py
# =============================================================================
"""Use Case: Execute Refactoring Plans"""

from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional

from ..services.execution_service import ExecutionService
from ..dto.analysis_result import ExecutionResult
from ...domain.entities.refactor_plan import RefactorPlan


@dataclass
class ExecuteRefactoringRequest:
    """Request for executing refactoring plans"""
    plans: List[RefactorPlan]
    backup: bool = True
    dry_run: bool = False
    verbose: bool = False


class ExecuteRefactoringUseCase:
    """Use case for executing refactoring plans"""
    
    def __init__(self, execution_service: ExecutionService):
        self.execution_service = execution_service
    
    def execute(self, request: ExecuteRefactoringRequest) -> ExecutionResult:
        """Execute the refactoring use case"""
        
        if request.verbose:
            mode = "DRY RUN" if request.dry_run else "LIVE EXECUTION"
            print(f"⚡ Executing refactoring plans - Mode: {mode}")
            print(f"   Plans to execute: {len(request.plans)}")
            print(f"   Backup enabled: {request.backup}")
        
        if request.dry_run:
            return self._simulate_execution(request)
        
        result = self.execution_service.execute_plans(
            request.plans,
            backup=request.backup
        )
        
        if request.verbose:
            print(f"\n✅ Execution complete!")
            print(f"   Successful: {result.successful}")
            print(f"   Failed: {result.failed}")
            print(f"   Files created: {result.files_created}")
            print(f"   Time: {result.execution_time:.2f}s")
        
        return result
    
    def _simulate_execution(self, request: ExecuteRefactoringRequest) -> ExecutionResult:
        """Simulate execution for dry run"""
        from datetime import datetime
        
        if request.verbose:
            print("\n🔍 DRY RUN - Simulating execution...\n")
            
            for plan in request.plans:
                print(f"Plan: {plan.id}")
                print(f"  Action: {plan.action.value}")
                print(f"  Source: {plan.source_file.name}")
                print(f"  Operations: {len(plan.operations)}")
                print()
        
        return ExecutionResult(
            total_executed=len(request.plans),
            successful=len(request.plans),
            failed=0,
            files_created=sum(len(p.operations) for p in request.plans),
            execution_time=0.0,
            timestamp=datetime.now()
        )
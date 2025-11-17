# =============================================================================
# src/application/use_cases/analyze_test_files.py
# =============================================================================
"""Use Case: Analyze Test Files"""

from pathlib import Path
from dataclasses import dataclass

from ..services.analysis_service import AnalysisService
from ..dto.analysis_result import AnalysisResult


@dataclass
class AnalyzeTestFilesRequest:
    """Request for analyzing test files"""
    root_directory: Path
    max_workers: int = 4
    verbose: bool = False


class AnalyzeTestFilesUseCase:
    """Use case for analyzing test files"""
    
    def __init__(self, analysis_service: AnalysisService):
        self.analysis_service = analysis_service
    
    def execute(self, request: AnalyzeTestFilesRequest) -> AnalysisResult:
        """Execute the analysis use case"""
        
        if request.verbose:
            print(f"🔍 Analyzing test files in {request.root_directory}")
            print(f"   Workers: {request.max_workers}")
        
        result = self.analysis_service.analyze_directory(
            request.root_directory
        )
        
        if request.verbose:
            print(f"\n✅ Analysis complete!")
            print(f"   Total files: {result.total_files}")
            print(f"   Analyzed: {result.analyzed_files}")
            print(f"   Candidates: {result.candidates_for_refactoring}")
            print(f"   Time: {result.execution_time:.2f}s")
        
        return result
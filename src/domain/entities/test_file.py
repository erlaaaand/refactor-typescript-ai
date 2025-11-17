# =============================================================================
# src/domain/entities/test_file.py
# =============================================================================
"""TestFile Entity - Core Business Entity"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path

from ..value_objects.complexity import Complexity
from ..value_objects.quality_score import QualityScore
from ..value_objects.file_metadata import FileMetadata


@dataclass
class TestFile:
    """
    TestFile Entity - Represents a test file with all its properties
    This is a rich domain entity with behavior, not just data
    """
    
    # Identity
    metadata: FileMetadata
    
    # Structure
    imports: List[str] = field(default_factory=list)
    mock_data: List[Dict] = field(default_factory=list)
    categories: List[str] = field(default_factory=list)
    test_cases: List[str] = field(default_factory=list)
    setup_hooks: List[str] = field(default_factory=list)
    
    # Metrics (calculated)
    complexity: Optional[Complexity] = None
    quality: Optional[QualityScore] = None
    
    # Analysis timestamp
    analyzed_at: datetime = field(default_factory=datetime.now)
    
    def calculate_complexity(self) -> Complexity:
        """Calculate and store complexity"""
        self.complexity = Complexity.from_metrics(
            lines=self.metadata.total_lines,
            categories=len(self.categories),
            tests=len(self.test_cases),
            mocks=len(self.mock_data),
            hooks=len(self.setup_hooks)
        )
        return self.complexity
    
    def calculate_quality(self, cyclomatic_complexity: int,
                          code_smells: int) -> QualityScore:
        """Calculate and store quality score"""
        assertion_ratio = self._calculate_assertion_ratio()
        has_structure = len(self.categories) > 0
        has_setup = len(self.setup_hooks) > 0
        
        self.quality = QualityScore.calculate(
            assertion_ratio=assertion_ratio,
            has_structure=has_structure,
            cyclomatic_complexity=cyclomatic_complexity,
            has_setup=has_setup,
            code_smells=code_smells
        )
        return self.quality
    
    def needs_refactoring(self) -> bool:
        """Determine if file needs refactoring"""
        if not self.complexity:
            self.calculate_complexity()
        
        return (
            self.complexity.needs_refactoring() or
            self.metadata.total_lines > 300 or
            len(self.categories) > 6
        )
    
    def get_refactoring_reason(self) -> str:
        """Get human-readable refactoring reason"""
        if not self.needs_refactoring():
            return "No refactoring needed"
        
        reasons = []
        
        if self.metadata.total_lines > 300:
            reasons.append(f"File too long ({self.metadata.total_lines} lines)")
        
        if len(self.categories) > 6:
            reasons.append(f"Too many categories ({len(self.categories)})")
        
        if len(self.test_cases) > 20:
            reasons.append(f"Too many test cases ({len(self.test_cases)})")
        
        if self.complexity and self.complexity.score >= 60:
            reasons.append(f"High complexity ({self.complexity.score:.1f})")
        
        return "; ".join(reasons)
    
    def recommend_action(self) -> str:
        """Recommend refactoring action"""
        if not self.needs_refactoring():
            return "keep_as_is"
        
        if len(self.categories) > 6:
            return "split_by_category"
        elif len(self.test_cases) > 20:
            return "split_by_concern"
        else:
            return "extract_shared"
    
    def _calculate_assertion_ratio(self) -> float:
        """Calculate ratio of assertions to tests"""
        if not self.test_cases:
            return 0.0
        # This would be calculated from actual test content
        # For now, return a default
        return 1.0
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization"""
        return {
            'path': str(self.metadata.path),
            'relative_path': str(self.metadata.relative_path),
            'module': self.metadata.module,
            'size': self.metadata.size_bytes,
            'lines': self.metadata.total_lines,
            'code_lines': self.metadata.code_lines,
            'categories': self.categories,
            'test_count': len(self.test_cases),
            'mock_count': len(self.mock_data),
            'complexity': {
                'score': self.complexity.score,
                'level': self.complexity.level.value
            } if self.complexity else None,
            'quality': {
                'score': self.quality.score,
                'level': self.quality.level.value
            } if self.quality else None,
            'needs_refactoring': self.needs_refactoring(),
            'refactoring_reason': self.get_refactoring_reason(),
            'recommended_action': self.recommend_action(),
            'analyzed_at': self.analyzed_at.isoformat()
        }
# =============================================================================
# src/domain/value_objects/quality_score.py
# =============================================================================
"""Quality Score Value Object"""

from dataclasses import dataclass
from enum import Enum


class QualityLevel(Enum):
    """Quality level enumeration"""
    EXCELLENT = "excellent"  # 80-100
    GOOD = "good"           # 60-79
    FAIR = "fair"           # 40-59
    POOR = "poor"           # 0-39


@dataclass(frozen=True)
class QualityScore:
    """Immutable quality score value object"""
    
    score: float  # 0-100
    level: QualityLevel
    
    def __post_init__(self):
        if not 0 <= self.score <= 100:
            raise ValueError(f"Score must be between 0-100, got {self.score}")
    
    @classmethod
    def from_score(cls, score: float) -> 'QualityScore':
        """Create quality score from numeric value"""
        if score >= 80:
            level = QualityLevel.EXCELLENT
        elif score >= 60:
            level = QualityLevel.GOOD
        elif score >= 40:
            level = QualityLevel.FAIR
        else:
            level = QualityLevel.POOR
        
        return cls(score=score, level=level)
    
    @classmethod
    def calculate(cls, assertion_ratio: float, has_structure: bool,
                  cyclomatic_complexity: int, has_setup: bool,
                  code_smells: int) -> 'QualityScore':
        """Calculate quality score from various factors"""
        score = 100.0
        
        # Penalty for code smells
        score -= code_smells * 5
        
        # Penalty for poor assertion ratio
        if assertion_ratio < 0.5:
            score -= 30
        elif assertion_ratio < 1.0:
            score -= 20
        
        # Bonus for good structure
        if has_structure:
            score += 10
        
        # Bonus for setup/teardown
        if has_setup:
            score += 5
        
        # Penalty for complexity
        if cyclomatic_complexity > 100:
            score -= 30
        elif cyclomatic_complexity > 50:
            score -= 15
        
        score = max(0.0, min(100.0, score))
        return cls.from_score(score)
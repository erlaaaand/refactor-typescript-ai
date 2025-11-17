# =============================================================================
# src/domain/value_objects/complexity.py
# =============================================================================
"""Complexity Value Object"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict


class ComplexityLevel(Enum):
    """Complexity level enumeration"""
    SIMPLE = "simple"
    MEDIUM = "medium"
    COMPLEX = "complex"


@dataclass(frozen=True)
class Complexity:
    """Immutable complexity value object"""
    
    score: float  # 0-100
    level: ComplexityLevel
    factors: Dict[str, float]
    
    def __post_init__(self):
        if not 0 <= self.score <= 100:
            raise ValueError(f"Score must be between 0-100, got {self.score}")
    
    @classmethod
    def from_metrics(cls, lines: int, categories: int, tests: int, 
                     mocks: int, hooks: int) -> 'Complexity':
        """Calculate complexity from metrics"""
        score = 0.0
        factors = {}
        
        # Lines factor (0-30)
        if lines > 500:
            factors['lines'] = 30.0
        elif lines > 300:
            factors['lines'] = 20.0
        elif lines > 150:
            factors['lines'] = 10.0
        else:
            factors['lines'] = 0.0
        score += factors['lines']
        
        # Categories factor (0-25)
        if categories > 10:
            factors['categories'] = 25.0
        elif categories > 6:
            factors['categories'] = 15.0
        elif categories > 3:
            factors['categories'] = 8.0
        else:
            factors['categories'] = 0.0
        score += factors['categories']
        
        # Tests factor (0-20)
        if tests > 30:
            factors['tests'] = 20.0
        elif tests > 20:
            factors['tests'] = 12.0
        elif tests > 10:
            factors['tests'] = 6.0
        else:
            factors['tests'] = 0.0
        score += factors['tests']
        
        # Mocks factor (0-15)
        if mocks > 5:
            factors['mocks'] = 15.0
        elif mocks > 3:
            factors['mocks'] = 10.0
        elif mocks > 0:
            factors['mocks'] = 5.0
        else:
            factors['mocks'] = 0.0
        score += factors['mocks']
        
        # Hooks factor (0-10)
        if hooks > 3:
            factors['hooks'] = 10.0
        elif hooks > 0:
            factors['hooks'] = 5.0
        else:
            factors['hooks'] = 0.0
        score += factors['hooks']
        
        # Determine level
        if score >= 60:
            level = ComplexityLevel.COMPLEX
        elif score >= 30:
            level = ComplexityLevel.MEDIUM
        else:
            level = ComplexityLevel.SIMPLE
        
        return cls(score=score, level=level, factors=factors)
    
    def is_complex(self) -> bool:
        """Check if complexity is high"""
        return self.level == ComplexityLevel.COMPLEX
    
    def needs_refactoring(self) -> bool:
        """Check if refactoring is recommended"""
        return self.score >= 50

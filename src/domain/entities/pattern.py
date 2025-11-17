# =============================================================================
# src/domain/entities/pattern.py
# =============================================================================
"""Pattern Entity - Represents learned patterns from test files"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum


class PatternType(Enum):
    """Types of patterns"""
    STRUCTURE = "structure"
    NAMING = "naming"
    ORGANIZATION = "organization"
    MOCK_USAGE = "mock_usage"
    TEST_STRATEGY = "test_strategy"


class PatternFrequency(Enum):
    """Pattern frequency levels"""
    RARE = "rare"          # < 10%
    OCCASIONAL = "occasional"  # 10-30%
    COMMON = "common"      # 30-60%
    FREQUENT = "frequent"  # 60-80%
    DOMINANT = "dominant"  # > 80%


@dataclass
class Pattern:
    """
    Pattern Entity - Represents a learned pattern from codebase
    """
    
    # Identity
    id: str
    type: PatternType
    name: str
    description: str
    
    # Pattern data
    examples: List[str] = field(default_factory=list)
    occurrences: int = 0
    total_files: int = 0
    
    # Analysis
    frequency: Optional[PatternFrequency] = None
    confidence: float = 0.0  # 0-1
    
    # Metadata
    discovered_at: datetime = field(default_factory=datetime.now)
    last_seen: datetime = field(default_factory=datetime.now)
    
    # Related patterns
    related_patterns: List[str] = field(default_factory=list)
    
    # Quality indicators
    is_good_practice: bool = True
    recommendation: Optional[str] = None
    
    def calculate_frequency(self) -> PatternFrequency:
        """Calculate pattern frequency"""
        if self.total_files == 0:
            return PatternFrequency.RARE
        
        percentage = (self.occurrences / self.total_files) * 100
        
        if percentage > 80:
            self.frequency = PatternFrequency.DOMINANT
        elif percentage > 60:
            self.frequency = PatternFrequency.FREQUENT
        elif percentage > 30:
            self.frequency = PatternFrequency.COMMON
        elif percentage > 10:
            self.frequency = PatternFrequency.OCCASIONAL
        else:
            self.frequency = PatternFrequency.RARE
        
        return self.frequency
    
    def calculate_confidence(self) -> float:
        """Calculate confidence score"""
        if self.total_files == 0:
            self.confidence = 0.0
            return self.confidence
        
        # Base confidence on frequency
        freq_score = self.occurrences / self.total_files
        
        # Adjust by number of examples
        example_score = min(len(self.examples) / 10, 1.0)
        
        # Combined score
        self.confidence = (freq_score * 0.7) + (example_score * 0.3)
        
        return self.confidence
    
    def add_occurrence(self, example: str):
        """Add a new occurrence of this pattern"""
        self.occurrences += 1
        self.last_seen = datetime.now()
        
        # Keep only recent examples (max 10)
        if len(self.examples) < 10:
            self.examples.append(example)
    
    def is_significant(self) -> bool:
        """Check if pattern is significant enough to recommend"""
        return (
            self.confidence >= 0.5 and
            self.occurrences >= 3 and
            self.frequency not in [PatternFrequency.RARE]
        )
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'type': self.type.value,
            'name': self.name,
            'description': self.description,
            'occurrences': self.occurrences,
            'total_files': self.total_files,
            'frequency': self.frequency.value if self.frequency else None,
            'confidence': self.confidence,
            'is_good_practice': self.is_good_practice,
            'recommendation': self.recommendation,
            'examples_count': len(self.examples),
            'discovered_at': self.discovered_at.isoformat(),
            'last_seen': self.last_seen.isoformat()
        }
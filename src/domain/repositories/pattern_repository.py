# =============================================================================
# src/domain/repositories/pattern_repository.py
# =============================================================================
"""Pattern Repository Interface"""

from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.pattern import Pattern, PatternType, PatternFrequency


class PatternRepository(ABC):
    """Abstract repository for Pattern entities"""
    
    @abstractmethod
    def find_by_id(self, pattern_id: str) -> Optional[Pattern]:
        """Find pattern by ID"""
        pass
    
    @abstractmethod
    def find_all(self) -> List[Pattern]:
        """Find all patterns"""
        pass
    
    @abstractmethod
    def find_by_type(self, pattern_type: PatternType) -> List[Pattern]:
        """Find patterns by type"""
        pass
    
    @abstractmethod
    def find_by_frequency(self, frequency: PatternFrequency) -> List[Pattern]:
        """Find patterns by frequency"""
        pass
    
    @abstractmethod
    def find_significant(self) -> List[Pattern]:
        """Find significant patterns (confidence >= 0.5)"""
        pass
    
    @abstractmethod
    def find_good_practices(self) -> List[Pattern]:
        """Find patterns marked as good practices"""
        pass
    
    @abstractmethod
    def save(self, pattern: Pattern) -> None:
        """Save pattern"""
        pass
    
    @abstractmethod
    def save_all(self, patterns: List[Pattern]) -> None:
        """Save multiple patterns"""
        pass
    
    @abstractmethod
    def delete(self, pattern_id: str) -> bool:
        """Delete pattern by ID"""
        pass
    
    @abstractmethod
    def update_occurrence(self, pattern_id: str, example: str) -> None:
        """Update pattern occurrence count and add example"""
        pass
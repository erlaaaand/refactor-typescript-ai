# =============================================================================
# src/infrastructure/parsers/base_parser.py
# =============================================================================
"""Base Parser Interface"""

from abc import ABC, abstractmethod
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class ParseResult:
    """Standardized parse result"""
    imports: List[str]
    mock_data: List[Dict]
    categories: List[str]
    test_cases: List[str]
    setup_hooks: List[str]
    complexity_metrics: Dict
    raw_data: Dict


class BaseParser(ABC):
    """Abstract base parser"""
    
    @abstractmethod
    def parse(self, content: str) -> ParseResult:
        """Parse content and return structured result"""
        pass
    
    @abstractmethod
    def can_parse(self, file_path: str) -> bool:
        """Check if parser can handle this file"""
        pass
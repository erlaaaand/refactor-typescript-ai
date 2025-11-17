# =============================================================================
# src/infrastructure/analyzers/base_analyzer.py
# =============================================================================
"""Base Analyzer Interface"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from ...domain.entities.test_file import TestFile


class BaseAnalyzer(ABC):
    """Abstract base class for code analyzers"""
    
    @abstractmethod
    def analyze(self, test_file: TestFile) -> Dict[str, Any]:
        """
        Analyze test file and return metrics
        
        Args:
            test_file: TestFile entity to analyze
            
        Returns:
            Dictionary containing analysis metrics
        """
        pass
    
    def supports(self, test_file: TestFile) -> bool:
        """
        Check if analyzer supports this test file
        
        Args:
            test_file: TestFile entity to check
            
        Returns:
            True if analyzer can analyze this file
        """
        return True
    
    def get_name(self) -> str:
        """Get analyzer name"""
        return self.__class__.__name__
    
    def get_version(self) -> str:
        """Get analyzer version"""
        return "1.0.0"
    
    def validate_input(self, test_file: TestFile) -> bool:
        """
        Validate input before analysis
        
        Args:
            test_file: TestFile entity to validate
            
        Returns:
            True if input is valid
            
        Raises:
            ValidationException: If input is invalid
        """
        if not test_file:
            raise ValueError("TestFile cannot be None")
        
        if not test_file.metadata:
            raise ValueError("TestFile must have metadata")
        
        return True
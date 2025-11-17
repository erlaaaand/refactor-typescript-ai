# =============================================================================
# src/infrastructure/analyzers/quality_analyzer.py
# =============================================================================
"""Quality Analyzer"""

from typing import List
from ...domain.entities.test_file import TestFile


class QualityAnalyzer:
    """Analyzes code quality"""
    
    def detect_smells(self, test_file: TestFile) -> List[str]:
        """Detect code smells in test file"""
        smells = []
        
        # Long test file
        if test_file.metadata.total_lines > 500:
            smells.append('long_test_file')
        
        # Too many categories
        if len(test_file.categories) > 10:
            smells.append('too_many_categories')
        
        # Too many test cases
        if len(test_file.test_cases) > 30:
            smells.append('too_many_test_cases')
        
        # No categories
        if not test_file.categories and len(test_file.test_cases) > 10:
            smells.append('no_categories')
        
        # Mock overload
        if len(test_file.mock_data) > 10:
            smells.append('mock_overload')
        
        # No setup with mocks
        if test_file.mock_data and not test_file.setup_hooks:
            smells.append('no_setup_with_mocks')
        
        return smells
    
    def calculate_maintainability_index(self, test_file: TestFile, cyclomatic_complexity: int) -> float:
        """Calculate maintainability index"""
        import math
        
        # Simplified MI calculation
        loc = max(1, test_file.metadata.code_lines)
        complexity = max(1, cyclomatic_complexity)
        
        # Halstead volume approximation
        volume = loc * math.log2(complexity + 1)
        
        # MI formula (simplified)
        mi = 171 - 5.2 * math.log(volume) - 0.23 * complexity - 16.2 * math.log(loc)
        
        # Normalize to 0-100
        return max(0, min(100, mi))
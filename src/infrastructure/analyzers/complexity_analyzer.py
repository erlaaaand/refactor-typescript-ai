# =============================================================================
# src/infrastructure/analyzers/complexity_analyzer.py
# =============================================================================
"""Complexity Analyzer"""

from typing import Dict
from ...domain.entities.test_file import TestFile
from ...domain.value_objects.complexity import Complexity


class ComplexityAnalyzer:
    """Analyzes code complexity"""
    
    def analyze(self, test_file: TestFile) -> Complexity:
        """Analyze complexity of test file"""
        return Complexity.from_metrics(
            lines=test_file.metadata.total_lines,
            categories=len(test_file.categories),
            tests=len(test_file.test_cases),
            mocks=len(test_file.mock_data),
            hooks=len(test_file.setup_hooks)
        )
    
    def calculate_cyclomatic_complexity(self, content: str) -> int:
        """Calculate cyclomatic complexity"""
        return (
            content.count('if ') +
            content.count('else ') +
            content.count('switch ') +
            content.count('for ') +
            content.count('while ') +
            content.count('&&') +
            content.count('||') +
            1
        )
# =============================================================================
# tests/unit/domain/test_complexity.py
# =============================================================================
"""Unit tests for Complexity value object"""

import pytest
from src.domain.value_objects.complexity import Complexity, ComplexityLevel


class TestComplexity:
    """Test Complexity value object"""
    
    def test_create_complexity(self):
        """Test creating complexity instance"""
        complexity = Complexity(
            score=45.0,
            level=ComplexityLevel.MEDIUM,
            factors={'lines': 20.0, 'categories': 15.0}
        )
        
        assert complexity.score == 45.0
        assert complexity.level == ComplexityLevel.MEDIUM
        assert complexity.factors['lines'] == 20.0
    
    def test_complexity_from_metrics_simple(self):
        """Test complexity calculation for simple file"""
        complexity = Complexity.from_metrics(
            lines=100,
            categories=2,
            tests=5,
            mocks=1,
            hooks=1
        )
        
        assert complexity.level == ComplexityLevel.SIMPLE
        assert complexity.score < 30
    
    def test_complexity_from_metrics_medium(self):
        """Test complexity calculation for medium file"""
        complexity = Complexity.from_metrics(
            lines=250,
            categories=5,
            tests=15,
            mocks=3,
            hooks=2
        )
        
        assert complexity.level == ComplexityLevel.MEDIUM
        assert 30 <= complexity.score < 60
    
    def test_complexity_from_metrics_complex(self):
        """Test complexity calculation for complex file"""
        complexity = Complexity.from_metrics(
            lines=600,
            categories=12,
            tests=35,
            mocks=8,
            hooks=4
        )
        
        assert complexity.level == ComplexityLevel.COMPLEX
        assert complexity.score >= 60
    
    def test_is_complex(self):
        """Test is_complex method"""
        simple = Complexity.from_metrics(100, 2, 5, 1, 1)
        complex_file = Complexity.from_metrics(600, 12, 35, 8, 4)
        
        assert not simple.is_complex()
        assert complex_file.is_complex()
    
    def test_needs_refactoring(self):
        """Test needs_refactoring method"""
        low_score = Complexity(
            score=45.0,
            level=ComplexityLevel.MEDIUM,
            factors={}
        )
        high_score = Complexity(
            score=65.0,
            level=ComplexityLevel.COMPLEX,
            factors={}
        )
        
        assert not low_score.needs_refactoring()
        assert high_score.needs_refactoring()
    
    def test_invalid_score(self):
        """Test that invalid score raises error"""
        with pytest.raises(ValueError):
            Complexity(
                score=150.0,
                level=ComplexityLevel.SIMPLE,
                factors={}
            )
# =============================================================================
# tests/unit/domain/test_quality_score.py
# =============================================================================
"""Unit tests for QualityScore value object"""

import pytest
from src.domain.value_objects.quality_score import QualityScore, QualityLevel


class TestQualityScore:
    """Test QualityScore value object"""
    
    def test_create_quality_score(self):
        """Test creating quality score instance"""
        score = QualityScore(score=75.0, level=QualityLevel.GOOD)
        
        assert score.score == 75.0
        assert score.level == QualityLevel.GOOD
    
    def test_from_score_excellent(self):
        """Test creating excellent quality score"""
        score = QualityScore.from_score(90.0)
        
        assert score.level == QualityLevel.EXCELLENT
        assert score.score == 90.0
    
    def test_from_score_good(self):
        """Test creating good quality score"""
        score = QualityScore.from_score(70.0)
        
        assert score.level == QualityLevel.GOOD
        assert 60 <= score.score < 80
    
    def test_from_score_fair(self):
        """Test creating fair quality score"""
        score = QualityScore.from_score(50.0)
        
        assert score.level == QualityLevel.FAIR
        assert 40 <= score.score < 60
    
    def test_from_score_poor(self):
        """Test creating poor quality score"""
        score = QualityScore.from_score(30.0)
        
        assert score.level == QualityLevel.POOR
        assert score.score < 40
    
    def test_calculate_with_good_metrics(self):
        """Test calculating quality with good metrics"""
        score = QualityScore.calculate(
            assertion_ratio=1.0,
            has_structure=True,
            cyclomatic_complexity=20,
            has_setup=True,
            code_smells=0
        )
        
        assert score.level in [QualityLevel.EXCELLENT, QualityLevel.GOOD]
        assert score.score >= 60
    
    def test_calculate_with_poor_metrics(self):
        """Test calculating quality with poor metrics"""
        score = QualityScore.calculate(
            assertion_ratio=0.3,
            has_structure=False,
            cyclomatic_complexity=150,
            has_setup=False,
            code_smells=5
        )
        
        assert score.level in [QualityLevel.POOR, QualityLevel.FAIR]
        assert score.score < 60
    
    def test_invalid_score_too_high(self):
        """Test that score above 100 raises error"""
        with pytest.raises(ValueError):
            QualityScore(score=150.0, level=QualityLevel.EXCELLENT)
    
    def test_invalid_score_negative(self):
        """Test that negative score raises error"""
        with pytest.raises(ValueError):
            QualityScore(score=-10.0, level=QualityLevel.POOR)
    
    def test_immutability(self):
        """Test that quality score is immutable"""
        score = QualityScore.from_score(75.0)
        
        with pytest.raises(AttributeError):
            score.score = 80.0
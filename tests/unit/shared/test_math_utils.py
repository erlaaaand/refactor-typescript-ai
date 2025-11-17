# =============================================================================
# tests/unit/shared/test_math_utils.py
# =============================================================================
"""Unit tests for MathUtils"""

import pytest
from src.shared.utils.math_utils import MathUtils


class TestMathUtils:
    """Test MathUtils"""
    
    def test_calculate_percentage(self):
        """Test calculating percentage"""
        assert MathUtils.calculate_percentage(25, 100) == 25.0
        assert MathUtils.calculate_percentage(50, 200) == 25.0
        assert MathUtils.calculate_percentage(0, 100) == 0.0
    
    def test_calculate_percentage_zero_total(self):
        """Test percentage with zero total"""
        assert MathUtils.calculate_percentage(10, 0) == 0.0
    
    def test_weighted_average(self):
        """Test weighted average"""
        values = [80, 90, 70]
        weights = [0.5, 0.3, 0.2]
        
        result = MathUtils.weighted_average(values, weights)
        expected = (80 * 0.5) + (90 * 0.3) + (70 * 0.2)
        
        assert abs(result - expected) < 0.01
    
    def test_weighted_average_empty(self):
        """Test weighted average with empty lists"""
        assert MathUtils.weighted_average([], []) == 0.0
    
    def test_normalize(self):
        """Test normalizing value"""
        assert MathUtils.normalize(50, 0, 100) == 0.5
        assert MathUtils.normalize(0, 0, 100) == 0.0
        assert MathUtils.normalize(100, 0, 100) == 1.0
    
    def test_normalize_same_min_max(self):
        """Test normalize with same min and max"""
        assert MathUtils.normalize(50, 50, 50) == 0.0
    
    def test_scale(self):
        """Test scaling value"""
        # Scale 50 from 0-100 to 0-10
        result = MathUtils.scale(50, (0, 100), (0, 10))
        assert result == 5.0
        
        # Scale 75 from 0-100 to 0-1
        result = MathUtils.scale(75, (0, 100), (0, 1))
        assert result == 0.75
    
    def test_clamp_within_range(self):
        """Test clamping value within range"""
        assert MathUtils.clamp(50, 0, 100) == 50
    
    def test_clamp_below_min(self):
        """Test clamping value below minimum"""
        assert MathUtils.clamp(-10, 0, 100) == 0
    
    def test_clamp_above_max(self):
        """Test clamping value above maximum"""
        assert MathUtils.clamp(150, 0, 100) == 100
    
    def test_mean(self):
        """Test calculating mean"""
        assert MathUtils.mean([1, 2, 3, 4, 5]) == 3.0
        assert MathUtils.mean([10, 20, 30]) == 20.0
    
    def test_mean_empty(self):
        """Test mean with empty list"""
        assert MathUtils.mean([]) == 0.0
    
    def test_median_odd_count(self):
        """Test median with odd number of values"""
        assert MathUtils.median([1, 2, 3, 4, 5]) == 3.0
        assert MathUtils.median([5, 1, 3]) == 3.0
    
    def test_median_even_count(self):
        """Test median with even number of values"""
        assert MathUtils.median([1, 2, 3, 4]) == 2.5
        assert MathUtils.median([10, 20, 30, 40]) == 25.0
    
    def test_standard_deviation(self):
        """Test calculating standard deviation"""
        values = [2, 4, 4, 4, 5, 5, 7, 9]
        std_dev = MathUtils.standard_deviation(values)
        assert std_dev > 0
        assert std_dev < 3  # Approximate check
    
    def test_percentile(self):
        """Test calculating percentile"""
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        
        assert MathUtils.percentile(values, 50) == 5.5  # Median
        assert MathUtils.percentile(values, 25) == 3.25
        assert MathUtils.percentile(values, 75) == 7.75
    
    def test_calculate_complexity_score(self):
        """Test calculating complexity score"""
        metrics = {
            'lines': 30.0,
            'categories': 15.0,
            'tests': 10.0
        }
        weights = {
            'lines': 0.4,
            'categories': 0.3,
            'tests': 0.3
        }
        
        score = MathUtils.calculate_complexity_score(metrics, weights)
        expected = (30 * 0.4) + (15 * 0.3) + (10 * 0.3)
        
        assert abs(score - expected) < 0.01
    
    def test_calculate_complexity_score_clamped(self):
        """Test complexity score is clamped to 0-100"""
        metrics = {'metric1': 200.0}
        weights = {'metric1': 1.0}
        
        score = MathUtils.calculate_complexity_score(metrics, weights)
        assert 0 <= score <= 100
    
    def test_round_to_precision(self):
        """Test rounding to precision"""
        assert MathUtils.round_to_precision(3.14159, 2) == 3.14
        assert MathUtils.round_to_precision(3.14159, 3) == 3.142
        assert MathUtils.round_to_precision(10.5, 0) == 10.0
    
    def test_safe_divide(self):
        """Test safe division"""
        assert MathUtils.safe_divide(10, 2) == 5.0
        assert MathUtils.safe_divide(10, 0) == 0.0
        assert MathUtils.safe_divide(10, 0, default=1.0) == 1.0
# =============================================================================
# src/shared/utils/math_utils.py
# =============================================================================
"""Mathematical utilities for metrics and calculations"""

import math
from typing import List, Dict, Tuple


class MathUtils:
    """Utility functions for mathematical operations"""
    
    @staticmethod
    def calculate_percentage(part: float, total: float) -> float:
        """Calculate percentage"""
        if total == 0:
            return 0.0
        return (part / total) * 100
    
    @staticmethod
    def weighted_average(values: List[float], weights: List[float]) -> float:
        """
        Calculate weighted average
        
        Args:
            values: List of values
            weights: List of weights (must sum to 1.0)
        """
        if not values or not weights or len(values) != len(weights):
            return 0.0
        
        return sum(v * w for v, w in zip(values, weights))
    
    @staticmethod
    def normalize(value: float, min_val: float, max_val: float) -> float:
        """Normalize value to 0-1 range"""
        if max_val == min_val:
            return 0.0
        return (value - min_val) / (max_val - min_val)
    
    @staticmethod
    def scale(value: float, from_range: Tuple[float, float],
              to_range: Tuple[float, float]) -> float:
        """Scale value from one range to another"""
        from_min, from_max = from_range
        to_min, to_max = to_range
        
        normalized = MathUtils.normalize(value, from_min, from_max)
        return to_min + (normalized * (to_max - to_min))
    
    @staticmethod
    def clamp(value: float, min_val: float, max_val: float) -> float:
        """Clamp value between min and max"""
        return max(min_val, min(value, max_val))
    
    @staticmethod
    def mean(values: List[float]) -> float:
        """Calculate arithmetic mean"""
        if not values:
            return 0.0
        return sum(values) / len(values)
    
    @staticmethod
    def median(values: List[float]) -> float:
        """Calculate median"""
        if not values:
            return 0.0
        
        sorted_values = sorted(values)
        n = len(sorted_values)
        mid = n // 2
        
        if n % 2 == 0:
            return (sorted_values[mid - 1] + sorted_values[mid]) / 2
        return sorted_values[mid]
    
    @staticmethod
    def standard_deviation(values: List[float]) -> float:
        """Calculate standard deviation"""
        if not values:
            return 0.0
        
        mean_val = MathUtils.mean(values)
        variance = sum((x - mean_val) ** 2 for x in values) / len(values)
        return math.sqrt(variance)
    
    @staticmethod
    def percentile(values: List[float], percentile: float) -> float:
        """
        Calculate percentile
        
        Args:
            values: List of values
            percentile: Percentile to calculate (0-100)
        """
        if not values:
            return 0.0
        
        sorted_values = sorted(values)
        index = (percentile / 100) * (len(sorted_values) - 1)
        
        if index.is_integer():
            return sorted_values[int(index)]
        
        lower = sorted_values[int(math.floor(index))]
        upper = sorted_values[int(math.ceil(index))]
        return lower + (upper - lower) * (index - math.floor(index))
    
    @staticmethod
    def calculate_complexity_score(metrics: Dict[str, float],
                                   weights: Dict[str, float]) -> float:
        """
        Calculate complexity score from metrics and weights
        
        Args:
            metrics: Dictionary of metric values
            weights: Dictionary of weights for each metric
        """
        score = 0.0
        
        for metric, value in metrics.items():
            weight = weights.get(metric, 0.0)
            score += value * weight
        
        return MathUtils.clamp(score, 0.0, 100.0)
    
    @staticmethod
    def exponential_decay(initial: float, decay_rate: float, 
                         time: float) -> float:
        """Calculate exponential decay"""
        return initial * math.exp(-decay_rate * time)
    
    @staticmethod
    def round_to_precision(value: float, precision: int = 2) -> float:
        """Round to specified decimal places"""
        return round(value, precision)
    
    @staticmethod
    def safe_divide(numerator: float, denominator: float,
                   default: float = 0.0) -> float:
        """Divide with protection against division by zero"""
        if denominator == 0:
            return default
        return numerator / denominator
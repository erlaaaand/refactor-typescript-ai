# =============================================================================
# src/interfaces/cli/commands/__init__.py
# =============================================================================
"""CLI Commands Package"""

from .analyze_command import AnalyzeCommand
from .learn_command import LearnCommand
from .practice_command import PracticeCommand
from .execute_command import ExecuteCommand

__all__ = [
    'AnalyzeCommand',
    'LearnCommand',
    'PracticeCommand',
    'ExecuteCommand'
]
# =============================================================================
# src/interfaces/__init__.py
# =============================================================================
"""
Interface Layer Package

This layer handles user interaction and external system integration.
It contains CLI commands, configuration management, and presentation logic.

Components:
- CLI: Command-line interface using Typer
- Config: Configuration loading and validation
- Presenters: Output formatting and display logic
"""

from .cli import app

__all__ = ['app']

__version__ = '2.1.0'
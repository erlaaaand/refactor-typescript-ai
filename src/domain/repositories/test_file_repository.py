# =============================================================================
# src/domain/repositories/test_file_repository.py
# =============================================================================
"""TestFile Repository Interface"""

from abc import ABC, abstractmethod
from typing import List, Optional
from pathlib import Path

from ..entities.test_file import TestFile


class TestFileRepository(ABC):
    """Abstract repository for TestFile entities"""
    
    @abstractmethod
    def find_by_path(self, path: Path) -> Optional[TestFile]:
        """Find test file by path"""
        pass
    
    @abstractmethod
    def find_all(self) -> List[TestFile]:
        """Find all test files"""
        pass
    
    @abstractmethod
    def find_by_module(self, module: str) -> List[TestFile]:
        """Find test files by module"""
        pass
    
    @abstractmethod
    def find_needing_refactoring(self) -> List[TestFile]:
        """Find files that need refactoring"""
        pass
    
    @abstractmethod
    def save(self, test_file: TestFile) -> None:
        """Save test file"""
        pass
    
    @abstractmethod
    def save_all(self, test_files: List[TestFile]) -> None:
        """Save multiple test files"""
        pass
# =============================================================================
# src/infrastructure/persistence/file_storage.py
# =============================================================================
"""File-based Storage for Test Files"""

import json
from pathlib import Path
from typing import List, Optional

from ...domain.entities.test_file import TestFile
from ...domain.repositories.test_file_repository import TestFileRepository


class FileTestFileRepository(TestFileRepository):
    """File-based implementation of TestFileRepository"""
    
    def __init__(self, storage_dir: Path):
        self.storage_dir = storage_dir
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self._cache: Dict[Path, TestFile] = {}
    
    def find_by_path(self, path: Path) -> Optional[TestFile]:
        """Find test file by path"""
        if path in self._cache:
            return self._cache[path]
        
        # Load from file
        file_id = self._path_to_id(path)
        storage_path = self.storage_dir / f"{file_id}.json"
        
        if storage_path.exists():
            data = json.loads(storage_path.read_text())
            # Deserialize and return
            # Implementation would reconstruct TestFile from dict
            return None
        
        return None
    
    def find_all(self) -> List[TestFile]:
        """Find all test files"""
        files = []
        
        all_files_path = self.storage_dir / "all_files.json"
        if all_files_path.exists():
            data = json.loads(all_files_path.read_text())
            # Deserialize list of test files
            # Implementation would reconstruct TestFile objects
        
        return files
    
    def find_by_module(self, module: str) -> List[TestFile]:
        """Find test files by module"""
        all_files = self.find_all()
        return [tf for tf in all_files if tf.metadata.module == module]
    
    def find_needing_refactoring(self) -> List[TestFile]:
        """Find files that need refactoring"""
        all_files = self.find_all()
        return [tf for tf in all_files if tf.needs_refactoring()]
    
    def save(self, test_file: TestFile) -> None:
        """Save test file"""
        self._cache[test_file.metadata.path] = test_file
    
    def save_all(self, test_files: List[TestFile]) -> None:
        """Save multiple test files"""
        for test_file in test_files:
            self.save(test_file)
        
        # Save to JSON
        all_data = [tf.to_dict() for tf in test_files]
        all_files_path = self.storage_dir / "all_files.json"
        all_files_path.write_text(json.dumps(all_data, indent=2))
        
        # Save candidates
        candidates = [tf for tf in test_files if tf.needs_refactoring()]
        candidates_data = [tf.to_dict() for tf in candidates]
        candidates_path = self.storage_dir / "candidates.json"
        candidates_path.write_text(json.dumps(candidates_data, indent=2))
    
    def _path_to_id(self, path: Path) -> str:
        """Convert path to storage ID"""
        return str(path).replace('/', '_').replace('\\', '_')
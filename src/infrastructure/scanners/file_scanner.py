# =============================================================================
# src/infrastructure/scanners/file_scanner.py
# =============================================================================
"""File Scanner - Scans directories for test files"""

from pathlib import Path
from typing import List, Set
from concurrent.futures import ThreadPoolExecutor


class FileScanner:
    """Scans directories for test files"""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.exclude_dirs = {'node_modules', 'dist', 'build', '.git', 'coverage'}
        self.patterns = ['*.spec.ts', '*.test.ts', '*.spec.tsx', '*.test.tsx']
    
    def scan(self, root_dir: Path) -> List[Path]:
        """Scan directory for test files"""
        test_files = []
        
        for path in root_dir.rglob('*'):
            if path.is_file() and self._should_include(path):
                test_files.append(path)
        
        return test_files
    
    def _should_include(self, path: Path) -> bool:
        """Check if file should be included"""
        # Check if in excluded directory
        if any(excluded in path.parts for excluded in self.exclude_dirs):
            return False
        
        # Check if matches pattern
        return any(path.match(pattern) for pattern in self.patterns)
    
    def _is_test_directory(self, path: Path) -> bool:
        """Check if directory is a test directory"""
        return '__tests__' in path.parts or 'test' in path.parts
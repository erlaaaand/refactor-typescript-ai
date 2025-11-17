# =============================================================================
# src/infrastructure/scanners/parallel_scanner.py
# =============================================================================
"""Parallel Scanner - Scans files using multiple workers"""

from pathlib import Path
from typing import List, Callable, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass


@dataclass
class ScanResult:
    """Result of scanning operation"""
    file_path: Path
    success: bool
    data: Optional[any] = None
    error: Optional[str] = None


class ParallelScanner:
    """Scans directories and processes files in parallel"""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
    
    def scan_and_process(
        self,
        root_dir: Path,
        patterns: List[str],
        processor: Callable[[Path], any],
        exclude_dirs: Optional[List[str]] = None
    ) -> List[ScanResult]:
        """
        Scan directory and process files in parallel
        
        Args:
            root_dir: Root directory to scan
            patterns: File patterns to match
            processor: Function to process each file
            exclude_dirs: Directories to exclude
        """
        if exclude_dirs is None:
            exclude_dirs = ['node_modules', 'dist', 'build', '.git']
        
        # Find all matching files
        files = self._find_files(root_dir, patterns, exclude_dirs)
        
        # Process in parallel
        results = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_file = {
                executor.submit(self._process_file, file_path, processor): file_path
                for file_path in files
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    results.append(ScanResult(
                        file_path=file_path,
                        success=False,
                        error=str(e)
                    ))
        
        return results
    
    def scan_batches(
        self,
        root_dir: Path,
        patterns: List[str],
        batch_size: int = 10,
        exclude_dirs: Optional[List[str]] = None
    ) -> List[List[Path]]:
        """
        Scan and return files in batches
        
        Args:
            root_dir: Root directory to scan
            patterns: File patterns to match
            batch_size: Number of files per batch
            exclude_dirs: Directories to exclude
        """
        files = self._find_files(root_dir, patterns, exclude_dirs)
        
        # Split into batches
        batches = []
        for i in range(0, len(files), batch_size):
            batch = files[i:i + batch_size]
            batches.append(batch)
        
        return batches
    
    def _find_files(
        self,
        root_dir: Path,
        patterns: List[str],
        exclude_dirs: List[str]
    ) -> List[Path]:
        """Find all files matching patterns"""
        files = []
        
        for pattern in patterns:
            for file_path in root_dir.rglob(pattern):
                # Check if in excluded directory
                if any(excluded in file_path.parts for excluded in exclude_dirs):
                    continue
                
                if file_path.is_file():
                    files.append(file_path)
        
        return files
    
    def _process_file(
        self,
        file_path: Path,
        processor: Callable[[Path], any]
    ) -> ScanResult:
        """Process a single file"""
        try:
            data = processor(file_path)
            return ScanResult(
                file_path=file_path,
                success=True,
                data=data
            )
        except Exception as e:
            return ScanResult(
                file_path=file_path,
                success=False,
                error=str(e)
            )
    
    def estimate_time(
        self,
        file_count: int,
        avg_processing_time: float
    ) -> float:
        """
        Estimate processing time
        
        Args:
            file_count: Number of files to process
            avg_processing_time: Average time per file in seconds
        """
        # With parallel processing, time is reduced by worker count
        sequential_time = file_count * avg_processing_time
        parallel_time = sequential_time / self.max_workers
        
        # Add overhead (10%)
        return parallel_time * 1.1
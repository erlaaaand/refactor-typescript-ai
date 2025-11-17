# =============================================================================
# src/shared/utils/file_utils.py
# =============================================================================
"""File utilities for common file operations"""

from pathlib import Path
from typing import List, Optional
import shutil
from datetime import datetime


class FileUtils:
    """Utility functions for file operations"""
    
    @staticmethod
    def ensure_directory(path: Path) -> Path:
        """Ensure directory exists, create if not"""
        path.mkdir(parents=True, exist_ok=True)
        return path
    
    @staticmethod
    def backup_file(file_path: Path, backup_dir: Optional[Path] = None) -> Path:
        """Create backup of file"""
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if backup_dir is None:
            backup_dir = file_path.parent / "backups"
        
        FileUtils.ensure_directory(backup_dir)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
        backup_path = backup_dir / backup_name
        
        shutil.copy2(file_path, backup_path)
        return backup_path
    
    @staticmethod
    def safe_write(file_path: Path, content: str, backup: bool = True) -> bool:
        """Safely write content to file with optional backup"""
        try:
            if file_path.exists() and backup:
                FileUtils.backup_file(file_path)
            
            FileUtils.ensure_directory(file_path.parent)
            file_path.write_text(content, encoding='utf-8')
            return True
        except Exception:
            return False
    
    @staticmethod
    def read_file(file_path: Path) -> str:
        """Read file content"""
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        return file_path.read_text(encoding='utf-8')
    
    @staticmethod
    def get_relative_path(file_path: Path, root: Path) -> Path:
        """Get relative path from root"""
        try:
            return file_path.relative_to(root)
        except ValueError:
            return file_path
    
    @staticmethod
    def find_files(directory: Path, patterns: List[str], 
                   exclude_dirs: List[str] = None) -> List[Path]:
        """Find files matching patterns"""
        if exclude_dirs is None:
            exclude_dirs = ['node_modules', 'dist', 'build']
        
        files = []
        for pattern in patterns:
            for file_path in directory.rglob(pattern):
                # Check if in excluded directory
                if any(excluded in file_path.parts for excluded in exclude_dirs):
                    continue
                
                if file_path.is_file():
                    files.append(file_path)
        
        return files
    
    @staticmethod
    def get_file_stats(file_path: Path) -> dict:
        """Get file statistics"""
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        stat = file_path.stat()
        content = FileUtils.read_file(file_path)
        lines = content.split('\n')
        
        return {
            'size_bytes': stat.st_size,
            'size_kb': stat.st_size / 1024,
            'total_lines': len(lines),
            'non_empty_lines': len([l for l in lines if l.strip()]),
            'last_modified': datetime.fromtimestamp(stat.st_mtime)
        }
    
    @staticmethod
    def clean_directory(directory: Path, keep_patterns: List[str] = None):
        """Clean directory keeping only specified patterns"""
        if not directory.exists():
            return
        
        if keep_patterns is None:
            keep_patterns = []
        
        for item in directory.iterdir():
            should_keep = any(item.match(pattern) for pattern in keep_patterns)
            
            if not should_keep:
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item)
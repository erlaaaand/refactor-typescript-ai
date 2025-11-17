# =============================================================================
"""File Utilities"""

from pathlib import Path
from datetime import datetime
import shutil
import os


class FileUtils:
    """Utility class for file operations"""
    
    @staticmethod
    def safe_write(file_path: Path, content: str, backup: bool = True) -> bool:
        """Safely write content to file with optional backup"""
        try:
            file_path = Path(file_path)
            
            # Create directory if it doesn't exist
            FileUtils.ensure_directory(file_path.parent)
            
            # Backup existing file if needed
            if file_path.exists() and backup:
                FileUtils.backup_file(file_path)
            
            # Write file
            file_path.write_text(content, encoding='utf-8')
            print(f"DEBUG FileUtils: Successfully wrote {len(content)} bytes to {file_path}")
            return True
            
        except Exception as e:
            print(f"DEBUG FileUtils: Failed to write {file_path}: {e}")
            return False
    
    @staticmethod
    def ensure_directory(directory: Path) -> bool:
        """Ensure directory exists"""
        try:
            directory.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            print(f"DEBUG FileUtils: Failed to create directory {directory}: {e}")
            return False
    
    @staticmethod
    def backup_file(file_path: Path) -> bool:
        """Create backup of file"""
        try:
            if not file_path.exists():
                return False
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = file_path.parent / f"{file_path.stem}_{timestamp}{file_path.suffix}"
            
            shutil.copy2(file_path, backup_path)
            return True
            
        except Exception as e:
            print(f"DEBUG FileUtils: Backup failed for {file_path}: {e}")
            return False
    
    @staticmethod
    def read_file(file_path: Path) -> str:
        """Read file content"""
        try:
            return file_path.read_text(encoding='utf-8')
        except Exception as e:
            print(f"DEBUG FileUtils: Failed to read {file_path}: {e}")
            return ""

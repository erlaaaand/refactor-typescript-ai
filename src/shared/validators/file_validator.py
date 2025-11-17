# =============================================================================
# src/shared/validators/file_validator.py
# =============================================================================
"""File Validator - Validates file operations"""

from pathlib import Path
from typing import List
from ..exceptions.base_exceptions import ValidationException


class FileValidator:
    """Validates file-related operations"""
    
    ALLOWED_EXTENSIONS = ['.ts', '.tsx', '.js', '.jsx']
    TEST_PATTERNS = ['spec', 'test']
    MAX_FILE_SIZE_MB = 10
    
    @staticmethod
    def validate_path(path: Path) -> bool:
        """Validate that path exists and is accessible"""
        if not isinstance(path, Path):
            raise ValidationException(
                "Invalid path type",
                {'expected': 'Path', 'got': type(path).__name__}
            )
        
        if not path.exists():
            raise ValidationException(
                "Path does not exist",
                {'path': str(path)}
            )
        
        return True
    
    @staticmethod
    def validate_file(path: Path) -> bool:
        """Validate that path is a valid file"""
        FileValidator.validate_path(path)
        
        if not path.is_file():
            raise ValidationException(
                "Path is not a file",
                {'path': str(path)}
            )
        
        return True
    
    @staticmethod
    def validate_directory(path: Path) -> bool:
        """Validate that path is a valid directory"""
        FileValidator.validate_path(path)
        
        if not path.is_dir():
            raise ValidationException(
                "Path is not a directory",
                {'path': str(path)}
            )
        
        return True
    
    @staticmethod
    def validate_test_file(path: Path) -> bool:
        """Validate that file is a test file"""
        FileValidator.validate_file(path)
        
        # Check extension
        if path.suffix not in FileValidator.ALLOWED_EXTENSIONS:
            raise ValidationException(
                "Invalid file extension",
                {
                    'path': str(path),
                    'extension': path.suffix,
                    'allowed': FileValidator.ALLOWED_EXTENSIONS
                }
            )
        
        # Check if it's a test file
        is_test = any(pattern in path.name.lower() 
                     for pattern in FileValidator.TEST_PATTERNS)
        
        if not is_test:
            raise ValidationException(
                "File is not a test file",
                {
                    'path': str(path),
                    'patterns': FileValidator.TEST_PATTERNS
                }
            )
        
        return True
    
    @staticmethod
    def validate_file_size(path: Path) -> bool:
        """Validate file size is within limits"""
        FileValidator.validate_file(path)
        
        size_mb = path.stat().st_size / (1024 * 1024)
        
        if size_mb > FileValidator.MAX_FILE_SIZE_MB:
            raise ValidationException(
                "File size exceeds limit",
                {
                    'path': str(path),
                    'size_mb': round(size_mb, 2),
                    'max_mb': FileValidator.MAX_FILE_SIZE_MB
                }
            )
        
        return True
    
    @staticmethod
    def validate_writable(path: Path) -> bool:
        """Validate that path is writable"""
        if path.exists():
            if not path.is_file():
                raise ValidationException(
                    "Path exists but is not a file",
                    {'path': str(path)}
                )
        else:
            # Check parent directory is writable
            parent = path.parent
            if not parent.exists():
                raise ValidationException(
                    "Parent directory does not exist",
                    {'path': str(path), 'parent': str(parent)}
                )
            
            if not parent.is_dir():
                raise ValidationException(
                    "Parent path is not a directory",
                    {'parent': str(parent)}
                )
        
        return True
    
    @staticmethod
    def validate_batch(paths: List[Path]) -> List[Path]:
        """Validate a batch of paths, return valid ones"""
        valid_paths = []
        
        for path in paths:
            try:
                FileValidator.validate_test_file(path)
                FileValidator.validate_file_size(path)
                valid_paths.append(path)
            except ValidationException:
                continue
        
        return valid_paths
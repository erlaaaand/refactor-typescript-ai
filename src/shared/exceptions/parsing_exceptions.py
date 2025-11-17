# =============================================================================
# src/shared/exceptions/parsing_exceptions.py
# =============================================================================
"""Parsing-specific Exceptions"""

from pathlib import Path
from typing import Optional
from .base_exceptions import InfrastructureException


class ParsingException(InfrastructureException):
    """Base exception for parsing errors"""
    
    def __init__(self, message: str, file_path: Optional[Path] = None, 
                 line_number: Optional[int] = None, cause: Exception = None):
        self.file_path = file_path
        self.line_number = line_number
        super().__init__(message, cause)
    
    def __str__(self):
        parts = [self.message]
        if self.file_path:
            parts.append(f"File: {self.file_path}")
        if self.line_number:
            parts.append(f"Line: {self.line_number}")
        return " | ".join(parts)


class SyntaxParsingException(ParsingException):
    """Raised when syntax parsing fails"""
    
    def __init__(self, message: str, file_path: Optional[Path] = None,
                 line_number: Optional[int] = None, syntax_error: str = ""):
        self.syntax_error = syntax_error
        super().__init__(message, file_path, line_number)


class ImportParsingException(ParsingException):
    """Raised when import statement parsing fails"""
    
    def __init__(self, message: str, import_statement: str = "",
                 file_path: Optional[Path] = None, line_number: Optional[int] = None):
        self.import_statement = import_statement
        super().__init__(message, file_path, line_number)


class MockParsingException(ParsingException):
    """Raised when mock data parsing fails"""
    
    def __init__(self, message: str, mock_name: str = "",
                 file_path: Optional[Path] = None, line_number: Optional[int] = None):
        self.mock_name = mock_name
        super().__init__(message, file_path, line_number)


class TestStructureParsingException(ParsingException):
    """Raised when test structure parsing fails"""
    
    def __init__(self, message: str, block_type: str = "",
                 file_path: Optional[Path] = None, line_number: Optional[int] = None):
        self.block_type = block_type
        super().__init__(message, file_path, line_number)


class UnsupportedFileTypeException(ParsingException):
    """Raised when file type is not supported"""
    
    def __init__(self, file_path: Path, supported_types: list):
        self.supported_types = supported_types
        message = f"Unsupported file type: {file_path.suffix}"
        super().__init__(message, file_path)
    
    def __str__(self):
        return f"{self.message} | Supported: {', '.join(self.supported_types)}"


class FileEncodingException(ParsingException):
    """Raised when file encoding is problematic"""
    
    def __init__(self, file_path: Path, encoding: str, cause: Exception = None):
        self.encoding = encoding
        message = f"Failed to read file with encoding: {encoding}"
        super().__init__(message, file_path, cause=cause)
# =============================================================================
# src/domain/value_objects/file_metadata.py
# =============================================================================
"""File Metadata Value Object"""

from dataclasses import dataclass
from pathlib import Path
from datetime import datetime


@dataclass(frozen=True)
class FileMetadata:
    """Immutable file metadata"""
    
    path: Path
    relative_path: Path
    module: str
    size_bytes: int
    total_lines: int
    code_lines: int
    comment_lines: int
    blank_lines: int
    last_modified: datetime
    
    @property
    def size_kb(self) -> float:
        """Size in kilobytes"""
        return self.size_bytes / 1024
    
    @property
    def code_density(self) -> float:
        """Ratio of code lines to total lines"""
        if self.total_lines == 0:
            return 0.0
        return self.code_lines / self.total_lines
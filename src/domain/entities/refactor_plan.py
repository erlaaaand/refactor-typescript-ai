# =============================================================================
# src/domain/entities/refactor_plan.py
# =============================================================================
"""RefactorPlan Entity - Represents a refactoring plan"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum
from pathlib import Path


class RefactorAction(Enum):
    """Types of refactoring actions"""
    SPLIT_BY_CATEGORY = "split_by_category"
    SPLIT_BY_CONCERN = "split_by_concern"
    EXTRACT_SHARED = "extract_shared"
    KEEP_AS_IS = "keep_as_is"
    CONSOLIDATE = "consolidate"


class PlanStatus(Enum):
    """Plan execution status"""
    DRAFT = "draft"
    READY = "ready"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class FileOperation:
    """Represents a file operation in the plan"""
    action: str  # create, modify, delete
    source_path: Optional[Path]
    target_path: Path
    content: Optional[str] = None
    reason: str = ""


@dataclass
class RefactorPlan:
    """
    RefactorPlan Entity - Represents a complete refactoring plan
    """
    
    # Identity
    id: str
    source_file: Path
    
    # Plan details
    action: RefactorAction
    reason: str
    description: str
    
    # Operations
    operations: List[FileOperation] = field(default_factory=list)
    
    # Metrics
    estimated_impact: Dict[str, int] = field(default_factory=dict)
    confidence: float = 0.0  # 0-1
    priority: int = 1  # 1-5
    
    # Status
    status: PlanStatus = PlanStatus.DRAFT
    created_at: datetime = field(default_factory=datetime.now)
    executed_at: Optional[datetime] = None
    
    # Results
    success: bool = False
    error_message: Optional[str] = None
    files_created: List[Path] = field(default_factory=list)
    files_modified: List[Path] = field(default_factory=list)
    files_deleted: List[Path] = field(default_factory=list)
    
    def add_operation(self, operation: FileOperation):
        """Add a file operation to the plan"""
        self.operations.append(operation)
    
    def calculate_estimated_impact(self):
        """Calculate estimated impact of refactoring"""
        self.estimated_impact = {
            'files_created': len([op for op in self.operations if op.action == 'create']),
            'files_modified': len([op for op in self.operations if op.action == 'modify']),
            'files_deleted': len([op for op in self.operations if op.action == 'delete']),
            'total_operations': len(self.operations)
        }
    
    def mark_ready(self):
        """Mark plan as ready for execution"""
        if not self.operations:
            raise ValueError("Cannot mark plan as ready: no operations defined")
        
        self.calculate_estimated_impact()
        self.status = PlanStatus.READY
    
    def mark_executing(self):
        """Mark plan as executing"""
        self.status = PlanStatus.EXECUTING
        self.executed_at = datetime.now()
    
    def mark_completed(self, files_created: List[Path], 
                      files_modified: List[Path],
                      files_deleted: List[Path]):
        """Mark plan as completed"""
        self.status = PlanStatus.COMPLETED
        self.success = True
        self.files_created = files_created
        self.files_modified = files_modified
        self.files_deleted = files_deleted
    
    def mark_failed(self, error_message: str):
        """Mark plan as failed"""
        self.status = PlanStatus.FAILED
        self.success = False
        self.error_message = error_message
    
    def mark_skipped(self, reason: str):
        """Mark plan as skipped"""
        self.status = PlanStatus.SKIPPED
        self.error_message = reason
    
    def is_executable(self) -> bool:
        """Check if plan can be executed"""
        return (
            self.status == PlanStatus.READY and
            len(self.operations) > 0 and
            self.confidence >= 0.5
        )
    
    def get_summary(self) -> str:
        """Get human-readable summary"""
        impact = self.estimated_impact or {}
        return (
            f"{self.action.value}: {self.source_file.name}\n"
            f"  Reason: {self.reason}\n"
            f"  Operations: {impact.get('total_operations', 0)}\n"
            f"  Confidence: {self.confidence:.2%}\n"
            f"  Status: {self.status.value}"
        )
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'source_file': str(self.source_file),
            'action': self.action.value,
            'reason': self.reason,
            'description': self.description,
            'operations': [
                {
                    'action': op.action,
                    'source': str(op.source_path) if op.source_path else None,
                    'target': str(op.target_path),
                    'reason': op.reason
                }
                for op in self.operations
            ],
            'estimated_impact': self.estimated_impact,
            'confidence': self.confidence,
            'priority': self.priority,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'executed_at': self.executed_at.isoformat() if self.executed_at else None,
            'success': self.success,
            'error_message': self.error_message
        }
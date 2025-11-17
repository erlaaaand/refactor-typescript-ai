# =============================================================================
# src/application/services/planning_service.py
# =============================================================================
"""Planning Service - Generates refactoring plans"""

from pathlib import Path
from typing import List, Dict
from datetime import datetime
import uuid

from ...domain.entities.test_file import TestFile
from ...domain.entities.refactor_plan import (
    RefactorPlan, RefactorAction, FileOperation
)
from ...domain.repositories.test_file_repository import TestFileRepository
from ..dto.analysis_result import PlanGenerationResult


class PlanningService:
    """Service for generating refactoring plans"""
    
    def __init__(self, repository: TestFileRepository):
        self.repository = repository
    
    def generate_plans(self, test_files: List[TestFile] = None) -> List[RefactorPlan]:
        """Generate refactoring plans for test files"""
        
        if test_files is None:
            test_files = self.repository.find_needing_refactoring()
        
        plans = []
        for test_file in test_files:
            if test_file.needs_refactoring():
                plan = self._create_plan_for_file(test_file)
                plans.append(plan)
        
        # Sort by priority
        plans.sort(key=lambda p: p.priority, reverse=True)
        
        return plans
    
    def generate_summary(self, plans: List[RefactorPlan]) -> PlanGenerationResult:
        """Generate summary of all plans"""
        
        action_counts = {}
        for plan in plans:
            action = plan.action.value
            action_counts[action] = action_counts.get(action, 0) + 1
        
        avg_confidence = sum(p.confidence for p in plans) / len(plans) if plans else 0
        
        return PlanGenerationResult(
            total_plans=len(plans),
            split_by_category=action_counts.get('split_by_category', 0),
            split_by_concern=action_counts.get('split_by_concern', 0),
            extract_shared=action_counts.get('extract_shared', 0),
            keep_as_is=action_counts.get('keep_as_is', 0),
            avg_confidence=avg_confidence,
            timestamp=datetime.now()
        )
    
    def _create_plan_for_file(self, test_file: TestFile) -> RefactorPlan:
        """Create a refactoring plan for a single file"""
        
        action = self._determine_action(test_file)
        plan_id = str(uuid.uuid4())[:8]
        
        plan = RefactorPlan(
            id=f"plan_{plan_id}",
            source_file=test_file.metadata.path,
            action=action,
            reason=test_file.get_refactoring_reason(),
            description=self._generate_description(test_file, action)
        )
        
        # Generate operations based on action
        if action == RefactorAction.SPLIT_BY_CATEGORY:
            self._plan_split_by_category(plan, test_file)
        elif action == RefactorAction.SPLIT_BY_CONCERN:
            self._plan_split_by_concern(plan, test_file)
        elif action == RefactorAction.EXTRACT_SHARED:
            self._plan_extract_shared(plan, test_file)
        
        # Calculate metrics
        plan.confidence = self._calculate_confidence(test_file, action)
        plan.priority = self._calculate_priority(test_file)
        plan.mark_ready()
        
        return plan
    
    def _determine_action(self, test_file: TestFile) -> RefactorAction:
        """Determine best refactoring action"""
        
        if len(test_file.categories) > 6:
            return RefactorAction.SPLIT_BY_CATEGORY
        elif len(test_file.test_cases) > 20:
            return RefactorAction.SPLIT_BY_CONCERN
        elif len(test_file.mock_data) > 5:
            return RefactorAction.EXTRACT_SHARED
        elif not test_file.needs_refactoring():
            return RefactorAction.KEEP_AS_IS
        else:
            return RefactorAction.SPLIT_BY_CONCERN
    
    def _generate_description(self, test_file: TestFile, 
                            action: RefactorAction) -> str:
        """Generate plan description"""
        
        descriptions = {
            RefactorAction.SPLIT_BY_CATEGORY: 
                f"Split {test_file.metadata.path.name} into {len(test_file.categories)} category-based files",
            RefactorAction.SPLIT_BY_CONCERN:
                f"Split {test_file.metadata.path.name} into separate test concerns",
            RefactorAction.EXTRACT_SHARED:
                f"Extract {len(test_file.mock_data)} mock utilities from {test_file.metadata.path.name}",
            RefactorAction.KEEP_AS_IS:
                f"Keep {test_file.metadata.path.name} as-is (well-organized)"
        }
        
        return descriptions.get(action, "Refactor test file")
    
    def _plan_split_by_category(self, plan: RefactorPlan, test_file: TestFile):
        """Plan splitting by category"""
        
        base_path = test_file.metadata.path.parent
        base_name = test_file.metadata.path.stem.replace('.spec', '').replace('.test', '')
        
        for category in test_file.categories:
            category_safe = category.lower().replace(' ', '-')
            new_file = base_path / f"{base_name}.{category_safe}.spec.ts"
            
            plan.add_operation(FileOperation(
                action='create',
                source_path=test_file.metadata.path,
                target_path=new_file,
                reason=f"Category: {category}"
            ))
    
    def _plan_split_by_concern(self, plan: RefactorPlan, test_file: TestFile):
        """Plan splitting by concern"""
        
        base_path = test_file.metadata.path.parent
        base_name = test_file.metadata.path.stem.replace('.spec', '').replace('.test', '')
        
        # Group tests by concern (simplified)
        num_files = min(3, max(2, len(test_file.test_cases) // 10))
        
        for i in range(num_files):
            new_file = base_path / f"{base_name}.part{i+1}.spec.ts"
            
            plan.add_operation(FileOperation(
                action='create',
                source_path=test_file.metadata.path,
                target_path=new_file,
                reason=f"Split part {i+1}"
            ))
    
    def _plan_extract_shared(self, plan: RefactorPlan, test_file: TestFile):
        """Plan extracting shared utilities"""
        
        base_path = test_file.metadata.path.parent
        utils_file = base_path / "test-utils.ts"
        
        plan.add_operation(FileOperation(
            action='create',
            source_path=None,
            target_path=utils_file,
            reason="Extract shared mock data and utilities"
        ))
        
        plan.add_operation(FileOperation(
            action='modify',
            source_path=test_file.metadata.path,
            target_path=test_file.metadata.path,
            reason="Update imports to use extracted utilities"
        ))
    
    def _calculate_confidence(self, test_file: TestFile, 
                            action: RefactorAction) -> float:
        """Calculate confidence for plan"""
        
        confidence = 0.5
        
        # Higher confidence for clear cases
        if action == RefactorAction.SPLIT_BY_CATEGORY and len(test_file.categories) > 8:
            confidence = 0.9
        elif action == RefactorAction.EXTRACT_SHARED and len(test_file.mock_data) > 7:
            confidence = 0.85
        elif test_file.complexity and test_file.complexity.score > 70:
            confidence = 0.8
        
        return confidence
    
    def _calculate_priority(self, test_file: TestFile) -> int:
        """Calculate priority (1-5, higher is more important)"""
        
        priority = 3  # Default
        
        if test_file.complexity and test_file.complexity.score > 80:
            priority = 5
        elif test_file.metadata.total_lines > 500:
            priority = 4
        elif len(test_file.categories) > 10:
            priority = 4
        
        return priority
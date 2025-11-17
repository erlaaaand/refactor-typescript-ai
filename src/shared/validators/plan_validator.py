# =============================================================================
# src/shared/validators/plan_validator.py
# =============================================================================
"""Plan Validator - Validates refactoring plans"""

from pathlib import Path
from typing import List
from ...domain.entities.refactor_plan import RefactorPlan, PlanStatus
from ..exceptions.base_exceptions import ValidationException


class PlanValidator:
    """Validates refactoring plans before execution"""
    
    MIN_CONFIDENCE = 0.3
    MAX_OPERATIONS = 50
    
    @staticmethod
    def validate_plan(plan: RefactorPlan) -> bool:
        """
        Validate a refactoring plan
        
        Args:
            plan: RefactorPlan to validate
            
        Returns:
            True if valid
            
        Raises:
            ValidationException: If validation fails
        """
        PlanValidator._validate_basic_info(plan)
        PlanValidator._validate_source_file(plan)
        PlanValidator._validate_operations(plan)
        PlanValidator._validate_confidence(plan)
        PlanValidator._validate_status(plan)
        
        return True
    
    @staticmethod
    def _validate_basic_info(plan: RefactorPlan):
        """Validate basic plan information"""
        if not plan.id:
            raise ValidationException("Plan ID cannot be empty")
        
        if not plan.description:
            raise ValidationException(
                "Plan description cannot be empty",
                {'plan_id': plan.id}
            )
        
        if not plan.reason:
            raise ValidationException(
                "Plan reason cannot be empty",
                {'plan_id': plan.id}
            )
    
    @staticmethod
    def _validate_source_file(plan: RefactorPlan):
        """Validate source file"""
        if not plan.source_file:
            raise ValidationException(
                "Source file cannot be None",
                {'plan_id': plan.id}
            )
        
        if not isinstance(plan.source_file, Path):
            raise ValidationException(
                "Source file must be a Path object",
                {'plan_id': plan.id, 'type': type(plan.source_file).__name__}
            )
        
        if not plan.source_file.exists():
            raise ValidationException(
                "Source file does not exist",
                {'plan_id': plan.id, 'path': str(plan.source_file)}
            )
    
    @staticmethod
    def _validate_operations(plan: RefactorPlan):
        """Validate plan operations"""
        if not plan.operations:
            raise ValidationException(
                "Plan must have at least one operation",
                {'plan_id': plan.id}
            )
        
        if len(plan.operations) > PlanValidator.MAX_OPERATIONS:
            raise ValidationException(
                f"Plan has too many operations (max: {PlanValidator.MAX_OPERATIONS})",
                {'plan_id': plan.id, 'count': len(plan.operations)}
            )
        
        # Validate each operation
        for i, operation in enumerate(plan.operations):
            if not operation.action:
                raise ValidationException(
                    f"Operation {i} missing action",
                    {'plan_id': plan.id}
                )
            
            if operation.action not in ['create', 'modify', 'delete']:
                raise ValidationException(
                    f"Invalid operation action: {operation.action}",
                    {'plan_id': plan.id, 'operation_index': i}
                )
            
            if not operation.target_path:
                raise ValidationException(
                    f"Operation {i} missing target path",
                    {'plan_id': plan.id}
                )
    
    @staticmethod
    def _validate_confidence(plan: RefactorPlan):
        """Validate confidence score"""
        if not 0 <= plan.confidence <= 1:
            raise ValidationException(
                "Confidence must be between 0 and 1",
                {'plan_id': plan.id, 'confidence': plan.confidence}
            )
        
        if plan.confidence < PlanValidator.MIN_CONFIDENCE:
            raise ValidationException(
                f"Confidence too low (min: {PlanValidator.MIN_CONFIDENCE})",
                {'plan_id': plan.id, 'confidence': plan.confidence}
            )
    
    @staticmethod
    def _validate_status(plan: RefactorPlan):
        """Validate plan status"""
        if plan.status not in [PlanStatus.DRAFT, PlanStatus.READY]:
            raise ValidationException(
                "Plan must be in DRAFT or READY status for validation",
                {'plan_id': plan.id, 'status': plan.status.value}
            )
    
    @staticmethod
    def validate_batch(plans: List[RefactorPlan]) -> List[RefactorPlan]:
        """
        Validate a batch of plans, return valid ones
        
        Args:
            plans: List of plans to validate
            
        Returns:
            List of valid plans
        """
        valid_plans = []
        
        for plan in plans:
            try:
                PlanValidator.validate_plan(plan)
                valid_plans.append(plan)
            except ValidationException:
                continue
        
        return valid_plans
    
    @staticmethod
    def check_conflicts(plans: List[RefactorPlan]) -> List[tuple]:
        """
        Check for conflicts between plans
        
        Returns:
            List of tuples (plan1_id, plan2_id, conflict_reason)
        """
        conflicts = []
        
        for i, plan1 in enumerate(plans):
            for plan2 in plans[i+1:]:
                # Check if plans target the same file
                if plan1.source_file == plan2.source_file:
                    conflicts.append((
                        plan1.id,
                        plan2.id,
                        f"Both plans target {plan1.source_file.name}"
                    ))
                
                # Check if plan operations overlap
                plan1_targets = {op.target_path for op in plan1.operations}
                plan2_targets = {op.target_path for op in plan2.operations}
                
                overlaps = plan1_targets & plan2_targets
                if overlaps:
                    conflicts.append((
                        plan1.id,
                        plan2.id,
                        f"Plans have overlapping target files: {overlaps}"
                    ))
        
        return conflicts
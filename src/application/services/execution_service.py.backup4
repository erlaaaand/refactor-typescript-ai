# =============================================================================
# src/application/services/execution_service.py
# =============================================================================
"""Execution Service - Executes refactoring plans"""

from pathlib import Path
from typing import List
from datetime import datetime
import shutil

from ...domain.entities.refactor_plan import RefactorPlan, FileOperation
from ...infrastructure.generators.code_generator import CodeGenerator
from ...shared.utils.file_utils import FileUtils
from ..dto.analysis_result import ExecutionResult


class ExecutionService:
    """Service for executing refactoring plans"""
    
    def __init__(self, code_generator: CodeGenerator):
        self.code_generator = code_generator
        self.file_utils = FileUtils()
    
    def execute_plans(self, plans: List[RefactorPlan], 
                     backup: bool = True) -> ExecutionResult:
        """Execute multiple refactoring plans"""
        
        start_time = datetime.now()
        successful = 0
        failed = 0
        files_created = 0
        
        for plan in plans:
            try:
                if not plan.is_executable():
                    continue
                
                # Backup if needed
                if backup and plan.source_file.exists():
                    self.file_utils.backup_file(plan.source_file)
                
                # Execute plan
                result = self._execute_single_plan(plan)
                
                if result:
                    successful += 1
                    files_created += len(plan.files_created)
                    plan.mark_completed(
                        plan.files_created,
                        plan.files_modified,
                        plan.files_deleted
                    )
                else:
                    failed += 1
                    plan.mark_failed("Execution failed")
                    
            except Exception as e:
                failed += 1
                plan.mark_failed(str(e))
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        return ExecutionResult(
            total_executed=len(plans),
            successful=successful,
            failed=failed,
            files_created=files_created,
            execution_time=execution_time,
            timestamp=datetime.now()
        )
    
    def _execute_single_plan(self, plan: RefactorPlan) -> bool:
        """Execute a single refactoring plan"""
        
        plan.mark_executing()
        
        try:
            for operation in plan.operations:
                self._execute_operation(operation, plan)
            
            return True
            
        except Exception:
            return False
    
    def _execute_operation(self, operation: FileOperation, plan: RefactorPlan):
        """Execute a single file operation"""
        
        if operation.action == 'create':
            self._create_file(operation, plan)
        elif operation.action == 'modify':
            self._modify_file(operation, plan)
        elif operation.action == 'delete':
            self._delete_file(operation, plan)
    
    def _create_file(self, operation: FileOperation, plan: RefactorPlan):
        """Create a new file"""
        
        # Generate content
        if operation.content:
            content = operation.content
        else:
            # Generate based on plan type
            content = self._generate_content_for_operation(operation, plan)
        
        # Write file
        self.file_utils.safe_write(operation.target_path, content, backup=False)
        plan.files_created.append(operation.target_path)
    
    def _modify_file(self, operation: FileOperation, plan: RefactorPlan):
        """Modify existing file"""
        
        if not operation.target_path.exists():
            return
        
        # Generate modified content
        content = self._generate_modified_content(operation, plan)
        
        # Write file
        self.file_utils.safe_write(operation.target_path, content, backup=True)
        plan.files_modified.append(operation.target_path)
    
    def _delete_file(self, operation: FileOperation, plan: RefactorPlan):
        """Delete a file"""
        
        if operation.target_path.exists():
            operation.target_path.unlink()
            plan.files_deleted.append(operation.target_path)
    
    def _generate_content_for_operation(self, operation: FileOperation,
                                       plan: RefactorPlan) -> str:
        """Generate content based on operation"""
        
        # Simple template for now
        header = self.code_generator.generate_file_header(
            f"Split from {plan.source_file.name} - {operation.reason}"
        )
        
        # Add basic structure
        content = header + "\n"
        content += "describe('Test Suite', () => {\n"
        content += "  it('should work', () => {\n"
        content += "    expect(true).toBe(true);\n"
        content += "  });\n"
        content += "});\n"
        
        return content
    
    def _generate_modified_content(self, operation: FileOperation,
                                  plan: RefactorPlan) -> str:
        """Generate modified content for file"""
        
        # Read original
        original = self.file_utils.read_file(operation.target_path)
        
        # Simple modification - add import for extracted utils
        if 'test-utils' in str(operation.target_path):
            import_line = "import { mockData } from './test-utils';\n"
            if import_line not in original:
                original = import_line + original
        
        return original
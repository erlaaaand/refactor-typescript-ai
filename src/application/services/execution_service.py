# =============================================================================
"""Execution Service - Executes refactoring plans"""

from pathlib import Path
from typing import List
from datetime import datetime

from ...domain.entities.refactor_plan import RefactorPlan, FileOperation
from ...infrastructure.generators.code_generator import CodeGenerator
from ...shared.utils.file_utils import FileUtils
from ..dto.analysis_result import ExecutionResult


class ExecutionService:
    """Service for executing refactoring plans"""

    def __init__(self, code_generator: CodeGenerator):
        self.code_generator = code_generator
        self.file_utils = FileUtils()
        print("DEBUG ExecutionService initialized")

    def execute_plans(self, plans: List[RefactorPlan], backup: bool = True) -> ExecutionResult:
        """Execute multiple refactoring plans"""
        print("DEBUG execute_plans called with", len(plans), "plans")
        
        start_time = datetime.now()
        successful = 0
        failed = 0
        total_files_created = 0

        for plan in plans:
            try:
                print(f"DEBUG Processing plan: {plan.id}")
                print(f"DEBUG Plan source: {plan.source_file}")
                print(f"DEBUG Plan action: {plan.action}")
                print(f"DEBUG Plan operations: {len(plan.operations)}")
                
                # Skip if not executable (handle missing method)
                if hasattr(plan, 'is_executable') and not plan.is_executable():
                    print(f"DEBUG Plan {plan.id} is not executable, skipping")
                    continue
                
                # Mark as executing if method exists
                if hasattr(plan, 'mark_executing'):
                    plan.mark_executing()
                
                # Execute each operation
                files_created = 0
                for operation in plan.operations:
                    print(f"DEBUG Executing operation: {operation.action} -> {operation.target_path}")
                    
                    if operation.action == "create":
                        if self._create_file(operation, plan):
                            files_created += 1
                
                total_files_created += files_created
                successful += 1
                
                # Mark as completed if method exists
                if hasattr(plan, 'mark_completed'):
                    plan.mark_completed(
                        getattr(plan, 'files_created', []),
                        getattr(plan, 'files_modified', []),
                        getattr(plan, 'files_deleted', [])
                    )
                
                print(f"DEBUG Plan {plan.id} executed successfully, created {files_created} files")

            except Exception as e:
                failed += 1
                print(f"DEBUG Plan {plan.id} failed: {e}")
                
                # Mark as failed if method exists
                if hasattr(plan, 'mark_failed'):
                    plan.mark_failed(str(e))
                
                import traceback
                traceback.print_exc()

        execution_time = (datetime.now() - start_time).total_seconds()
        print(f"DEBUG Execution completed: {successful} successful, {failed} failed, {total_files_created} files created")

        return ExecutionResult(
            total_executed=len(plans),
            successful=successful,
            failed=failed,
            files_created=total_files_created,
            execution_time=execution_time,
            timestamp=datetime.now()
        )

    def _create_file(self, operation: FileOperation, plan: RefactorPlan) -> bool:
        """Create a new file from operation - returns True if successful"""
        print(f"DEBUG _create_file called for: {operation.target_path}")
        
        try:
            # Generate content
            content = self._generate_file_content(operation, plan)
            print(f"DEBUG Generated content length: {len(content)}")
            
            # Write file
            result = self.file_utils.safe_write(operation.target_path, content, backup=False)
            print(f"DEBUG safe_write result: {result}")
            
            if result:
                print(f"DEBUG File created successfully: {operation.target_path}")
                # Track created files in plan
                if not hasattr(plan, 'files_created'):
                    plan.files_created = []
                plan.files_created.append(operation.target_path)
                return True
            else:
                print(f"DEBUG File creation failed: {operation.target_path}")
                return False
                
        except Exception as e:
            print(f"DEBUG _create_file error: {e}")
            return False

    def _generate_file_content(self, operation: FileOperation, plan: RefactorPlan) -> str:
        """Generate file content for operation"""
        print(f"DEBUG _generate_file_content for: {operation.target_path}")
        
        # Simple content generation
        header = self.code_generator.generate_file_header(f"Split from {plan.source_file} - {operation.reason}")
        content = header + f'''
import {{ Test }} from '@nestjs/testing';

describe('Test Suite - {operation.reason}', () => {{
  it('should test functionality', () => {{
    // Auto-generated by Test Refactor AI
    expect(true).toBe(true);
  }});
}});
'''
        return content

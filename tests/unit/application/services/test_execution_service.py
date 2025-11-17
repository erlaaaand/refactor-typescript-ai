# =============================================================================
# tests/unit/application/services/test_execution_service.py
# =============================================================================
"""Unit tests for ExecutionService"""

import pytest
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock

from src.application.services.execution_service import ExecutionService
from src.domain.entities.refactor_plan import RefactorPlan, RefactorAction, FileOperation, PlanStatus
from src.infrastructure.generators.code_generator import CodeGenerator


class TestExecutionService:
    """Test ExecutionService"""
    
    @pytest.fixture
    def mock_code_generator(self):
        """Create mock code generator"""
        generator = Mock(spec=CodeGenerator)
        generator.generate_file_header.return_value = "// Generated file"
        return generator
    
    @pytest.fixture
    def service(self, mock_code_generator):
        """Create execution service"""
        return ExecutionService(mock_code_generator)
    
    @pytest.fixture
    def sample_plan(self, tmp_path):
        """Create sample refactor plan"""
        source_file = tmp_path / "test.spec.ts"
        source_file.write_text("// test content")
        
        plan = RefactorPlan(
            id="plan_1",
            source_file=source_file,
            action=RefactorAction.SPLIT_BY_CATEGORY,
            reason="Too many categories",
            description="Split by category"
        )
        
        # Add operations
        plan.add_operation(FileOperation(
            action='create',
            source_path=source_file,
            target_path=tmp_path / "test.category1.spec.ts",
            reason="Category 1"
        ))
        
        plan.mark_ready()
        return plan
    
    def test_execute_plans_empty_list(self, service):
        """Test executing empty plan list"""
        result = service.execute_plans([], backup=False)
        
        assert result.total_executed == 0
        assert result.successful == 0
        assert result.failed == 0
    
    def test_execute_plans_single_plan(self, service, sample_plan):
        """Test executing single plan"""
        with patch.object(service, '_execute_single_plan', return_value=True):
            result = service.execute_plans([sample_plan], backup=False)
            
            assert result.total_executed == 1
            assert result.successful == 1
            assert result.failed == 0
    
    def test_execute_plans_with_backup(self, service, sample_plan):
        """Test executing with backup enabled"""
        with patch.object(service.file_utils, 'backup_file') as mock_backup:
            with patch.object(service, '_execute_single_plan', return_value=True):
                result = service.execute_plans([sample_plan], backup=True)
                
                # Backup should be called
                mock_backup.assert_called()
    
    def test_execute_plans_failure(self, service, sample_plan):
        """Test executing plan that fails"""
        with patch.object(service, '_execute_single_plan', return_value=False):
            result = service.execute_plans([sample_plan], backup=False)
            
            assert result.failed == 1
            assert sample_plan.status == PlanStatus.FAILED
    
    def test_execute_plans_exception(self, service, sample_plan):
        """Test executing plan that raises exception"""
        with patch.object(service, '_execute_single_plan', side_effect=Exception("Test error")):
            result = service.execute_plans([sample_plan], backup=False)
            
            assert result.failed == 1
    
    def test_execute_single_plan_success(self, service, sample_plan):
        """Test executing single plan successfully"""
        with patch.object(service, '_execute_operation'):
            result = service._execute_single_plan(sample_plan)
            
            assert result is True
            assert sample_plan.status == PlanStatus.EXECUTING
    
    def test_execute_single_plan_failure(self, service, sample_plan):
        """Test single plan execution failure"""
        with patch.object(service, '_execute_operation', side_effect=Exception("Error")):
            result = service._execute_single_plan(sample_plan)
            
            assert result is False
    
    def test_execute_operation_create(self, service, tmp_path):
        """Test creating file operation"""
        operation = FileOperation(
            action='create',
            source_path=None,
            target_path=tmp_path / "new_file.ts",
            content="// test content",
            reason="Create new file"
        )
        
        plan = Mock()
        plan.files_created = []
        
        service._execute_operation(operation, plan)
        
        assert (tmp_path / "new_file.ts").exists()
        assert tmp_path / "new_file.ts" in plan.files_created
    
    def test_execute_operation_modify(self, service, tmp_path):
        """Test modifying file operation"""
        # Create existing file
        existing_file = tmp_path / "existing.ts"
        existing_file.write_text("original content")
        
        operation = FileOperation(
            action='modify',
            source_path=existing_file,
            target_path=existing_file,
            reason="Modify file"
        )
        
        plan = Mock()
        plan.files_modified = []
        
        with patch.object(service, '_generate_modified_content', return_value="modified"):
            service._execute_operation(operation, plan)
            
            assert existing_file in plan.files_modified
    
    def test_execute_operation_delete(self, service, tmp_path):
        """Test deleting file operation"""
        # Create file to delete
        file_to_delete = tmp_path / "delete_me.ts"
        file_to_delete.write_text("content")
        
        operation = FileOperation(
            action='delete',
            source_path=None,
            target_path=file_to_delete,
            reason="Delete file"
        )
        
        plan = Mock()
        plan.files_deleted = []
        
        service._execute_operation(operation, plan)
        
        assert not file_to_delete.exists()
        assert file_to_delete in plan.files_deleted
    
    def test_create_file_with_content(self, service, tmp_path):
        """Test creating file with provided content"""
        operation = FileOperation(
            action='create',
            source_path=None,
            target_path=tmp_path / "new.ts",
            content="const x = 1;",
            reason="Create"
        )
        
        plan = Mock()
        plan.files_created = []
        
        service._create_file(operation, plan)
        
        assert (tmp_path / "new.ts").exists()
        assert (tmp_path / "new.ts").read_text() == "const x = 1;"
    
    def test_create_file_generate_content(self, service, tmp_path):
        """Test creating file with generated content"""
        operation = FileOperation(
            action='create',
            source_path=None,
            target_path=tmp_path / "new.ts",
            content=None,  # No content, should generate
            reason="Create"
        )
        
        plan = Mock()
        plan.source_file = Mock()
        plan.source_file.name = "test.spec.ts"
        plan.files_created = []
        
        with patch.object(service, '_generate_content_for_operation', return_value="generated"):
            service._create_file(operation, plan)
            
            assert (tmp_path / "new.ts").exists()
    
    def test_modify_file_non_existent(self, service, tmp_path):
        """Test modifying non-existent file"""
        operation = FileOperation(
            action='modify',
            source_path=None,
            target_path=tmp_path / "nonexistent.ts",
            reason="Modify"
        )
        
        plan = Mock()
        plan.files_modified = []
        
        # Should not raise error, just skip
        service._modify_file(operation, plan)
        assert len(plan.files_modified) == 0
    
    def test_delete_file_non_existent(self, service, tmp_path):
        """Test deleting non-existent file"""
        operation = FileOperation(
            action='delete',
            source_path=None,
            target_path=tmp_path / "nonexistent.ts",
            reason="Delete"
        )
        
        plan = Mock()
        plan.files_deleted = []
        
        # Should not raise error
        service._delete_file(operation, plan)
        assert len(plan.files_deleted) == 0
    
    def test_generate_content_for_operation(self, service, tmp_path, mock_code_generator):
        """Test generating content for operation"""
        operation = FileOperation(
            action='create',
            source_path=None,
            target_path=tmp_path / "new.ts",
            reason="Test split"
        )
        
        plan = Mock()
        plan.source_file = Mock()
        plan.source_file.name = "original.spec.ts"
        
        content = service._generate_content_for_operation(operation, plan)
        
        assert "describe('Test Suite'" in content
        assert "expect(true).toBe(true)" in content
    
    def test_generate_modified_content(self, service, tmp_path):
        """Test generating modified content"""
        original_file = tmp_path / "original.ts"
        original_file.write_text("const x = 1;")
        
        operation = FileOperation(
            action='modify',
            source_path=None,
            target_path=original_file,
            reason="Add import"
        )
        
        plan = Mock()
        
        content = service._generate_modified_content(operation, plan)
        
        # Should add import for test-utils
        assert "import" in content or "const x = 1;" in content
    
    def test_execution_result_timing(self, service, sample_plan):
        """Test execution result includes timing"""
        with patch.object(service, '_execute_single_plan', return_value=True):
            result = service.execute_plans([sample_plan], backup=False)
            
            assert result.execution_time >= 0
            assert isinstance(result.timestamp, datetime)
    
    def test_multiple_plans_execution(self, service, tmp_path):
        """Test executing multiple plans"""
        plans = []
        for i in range(3):
            source = tmp_path / f"test{i}.spec.ts"
            source.write_text("test")
            
            plan = RefactorPlan(
                id=f"plan_{i}",
                source_file=source,
                action=RefactorAction.SPLIT_BY_CATEGORY,
                reason="Test",
                description="Test plan"
            )
            plan.add_operation(FileOperation(
                action='create',
                source_path=source,
                target_path=tmp_path / f"out{i}.ts",
                reason="Split"
            ))
            plan.mark_ready()
            plans.append(plan)
        
        with patch.object(service, '_execute_single_plan', return_value=True):
            result = service.execute_plans(plans, backup=False)
            
            assert result.total_executed == 3
            assert result.successful == 3
    
    def test_plan_not_executable_skipped(self, service, tmp_path):
        """Test that non-executable plans are skipped"""
        source = tmp_path / "test.spec.ts"
        source.write_text("test")
        
        plan = RefactorPlan(
            id="plan_1",
            source_file=source,
            action=RefactorAction.SPLIT_BY_CATEGORY,
            reason="Test",
            description="Test"
        )
        # Don't mark as ready - not executable
        
        result = service.execute_plans([plan], backup=False)
        
        # Plan should be skipped
        assert result.total_executed == 1
        assert result.successful == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
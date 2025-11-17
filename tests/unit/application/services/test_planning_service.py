# =============================================================================
# tests/unit/application/services/test_planning_service.py
# =============================================================================
"""Unit tests for PlanningService"""

import pytest
from pathlib import Path
from unittest.mock import Mock, MagicMock
from datetime import datetime

from src.application.services.planning_service import PlanningService
from src.domain.entities.test_file import TestFile
from src.domain.entities.refactor_plan import RefactorPlan, RefactorAction
from src.domain.value_objects.file_metadata import FileMetadata
from src.domain.value_objects.complexity import Complexity, ComplexityLevel


class TestPlanningService:
    """Test PlanningService"""
    
    @pytest.fixture
    def mock_repository(self):
        """Create mock repository"""
        repo = Mock()
        repo.find_needing_refactoring = Mock(return_value=[])
        return repo
    
    @pytest.fixture
    def service(self, mock_repository):
        """Create planning service"""
        return PlanningService(mock_repository)
    
    @pytest.fixture
    def sample_test_file(self, tmp_path):
        """Create sample test file"""
        file_path = tmp_path / "test.spec.ts"
        file_path.write_text("test content")
        
        metadata = FileMetadata(
            path=file_path,
            relative_path=Path("src/test.spec.ts"),
            module="test",
            size_bytes=1000,
            total_lines=400,
            code_lines=300,
            comment_lines=50,
            blank_lines=50,
            last_modified=datetime.now()
        )
        
        test_file = TestFile(
            metadata=metadata,
            categories=[f"Category {i}" for i in range(8)],
            test_cases=[f"test {i}" for i in range(25)],
            mock_data=[{"name": f"mock{i}"} for i in range(6)]
        )
        
        test_file.calculate_complexity()
        return test_file
    
    def test_generate_plans_empty_list(self, service):
        """Test generating plans with empty list"""
        plans = service.generate_plans([])
        assert len(plans) == 0
    
    def test_generate_plans_from_repository(self, service, sample_test_file, mock_repository):
        """Test generating plans from repository"""
        mock_repository.find_needing_refactoring.return_value = [sample_test_file]
        
        plans = service.generate_plans()
        
        assert len(plans) == 1
        assert isinstance(plans[0], RefactorPlan)
    
    def test_generate_plans_with_test_files(self, service, sample_test_file):
        """Test generating plans with provided test files"""
        plans = service.generate_plans([sample_test_file])
        
        assert len(plans) == 1
        assert plans[0].source_file == sample_test_file.metadata.path
    
    def test_plans_sorted_by_priority(self, service, tmp_path):
        """Test plans are sorted by priority"""
        # Create files with different priorities
        files = []
        for i, lines in enumerate([600, 200, 400]):  # Different complexity
            path = tmp_path / f"test{i}.spec.ts"
            path.write_text("test")
            
            metadata = FileMetadata(
                path=path,
                relative_path=Path(f"test{i}.spec.ts"),
                module="test",
                size_bytes=1000,
                total_lines=lines,
                code_lines=lines-50,
                comment_lines=20,
                blank_lines=30,
                last_modified=datetime.now()
            )
            
            test_file = TestFile(metadata=metadata, categories=["Test"])
            test_file.calculate_complexity()
            files.append(test_file)
        
        plans = service.generate_plans(files)
        
        # Check sorted by priority (high priority first)
        assert len(plans) == 3
        # Highest priority should be first (600 lines)
        assert plans[0].priority >= plans[-1].priority
    
    def test_generate_summary(self, service, sample_test_file):
        """Test generating summary"""
        plans = service.generate_plans([sample_test_file])
        summary = service.generate_summary(plans)
        
        assert summary.total_plans == 1
        assert 0 <= summary.avg_confidence <= 1
        assert isinstance(summary.timestamp, datetime)
    
    def test_summary_action_counts(self, service, tmp_path):
        """Test summary counts actions correctly"""
        files = []
        
        # Create file needing split by category
        path1 = tmp_path / "test1.spec.ts"
        path1.write_text("test")
        metadata1 = FileMetadata(
            path=path1, relative_path=Path("test1.spec.ts"), module="test",
            size_bytes=1000, total_lines=300, code_lines=250,
            comment_lines=25, blank_lines=25, last_modified=datetime.now()
        )
        file1 = TestFile(
            metadata=metadata1,
            categories=[f"Cat{i}" for i in range(8)]  # Many categories
        )
        files.append(file1)
        
        # Create file needing split by concern
        path2 = tmp_path / "test2.spec.ts"
        path2.write_text("test")
        metadata2 = FileMetadata(
            path=path2, relative_path=Path("test2.spec.ts"), module="test",
            size_bytes=1000, total_lines=300, code_lines=250,
            comment_lines=25, blank_lines=25, last_modified=datetime.now()
        )
        file2 = TestFile(
            metadata=metadata2,
            categories=["Tests"],
            test_cases=[f"test{i}" for i in range(25)]  # Many tests
        )
        files.append(file2)
        
        plans = service.generate_plans(files)
        summary = service.generate_summary(plans)
        
        assert summary.split_by_category >= 1
        assert summary.split_by_concern >= 1
    
    def test_determine_action_split_by_category(self, service, sample_test_file):
        """Test determining split by category action"""
        # File has 8 categories (> 6)
        action = service._determine_action(sample_test_file)
        assert action == RefactorAction.SPLIT_BY_CATEGORY
    
    def test_determine_action_split_by_concern(self, service, tmp_path):
        """Test determining split by concern action"""
        path = tmp_path / "test.spec.ts"
        path.write_text("test")
        
        metadata = FileMetadata(
            path=path, relative_path=Path("test.spec.ts"), module="test",
            size_bytes=1000, total_lines=300, code_lines=250,
            comment_lines=25, blank_lines=25, last_modified=datetime.now()
        )
        
        test_file = TestFile(
            metadata=metadata,
            categories=["Tests"],
            test_cases=[f"test{i}" for i in range(25)]  # > 20 tests
        )
        
        action = service._determine_action(test_file)
        assert action == RefactorAction.SPLIT_BY_CONCERN
    
    def test_determine_action_extract_shared(self, service, tmp_path):
        """Test determining extract shared action"""
        path = tmp_path / "test.spec.ts"
        path.write_text("test")
        
        metadata = FileMetadata(
            path=path, relative_path=Path("test.spec.ts"), module="test",
            size_bytes=1000, total_lines=200, code_lines=150,
            comment_lines=25, blank_lines=25, last_modified=datetime.now()
        )
        
        test_file = TestFile(
            metadata=metadata,
            categories=["Tests"],
            mock_data=[{"name": f"mock{i}"} for i in range(8)]  # > 5 mocks
        )
        
        action = service._determine_action(test_file)
        assert action == RefactorAction.EXTRACT_SHARED
    
    def test_determine_action_keep_as_is(self, service, tmp_path):
        """Test determining keep as is action"""
        path = tmp_path / "test.spec.ts"
        path.write_text("test")
        
        metadata = FileMetadata(
            path=path, relative_path=Path("test.spec.ts"), module="test",
            size_bytes=500, total_lines=100, code_lines=80,
            comment_lines=10, blank_lines=10, last_modified=datetime.now()
        )
        
        test_file = TestFile(
            metadata=metadata,
            categories=["Tests"],
            test_cases=["test1", "test2"]
        )
        test_file.complexity = Complexity(
            score=20.0,
            level=ComplexityLevel.SIMPLE,
            factors={}
        )
        
        action = service._determine_action(test_file)
        assert action == RefactorAction.KEEP_AS_IS
    
    def test_generate_description(self, service, sample_test_file):
        """Test generating plan description"""
        action = RefactorAction.SPLIT_BY_CATEGORY
        description = service._generate_description(sample_test_file, action)
        
        assert sample_test_file.metadata.path.name in description
        assert "8" in description  # Number of categories
    
    def test_plan_split_by_category(self, service, sample_test_file):
        """Test planning split by category"""
        plan = RefactorPlan(
            id="test_plan",
            source_file=sample_test_file.metadata.path,
            action=RefactorAction.SPLIT_BY_CATEGORY,
            reason="Test",
            description="Test"
        )
        
        service._plan_split_by_category(plan, sample_test_file)
        
        # Should create operations for each category
        assert len(plan.operations) == len(sample_test_file.categories)
        assert all(op.action == 'create' for op in plan.operations)
    
    def test_plan_split_by_concern(self, service, sample_test_file):
        """Test planning split by concern"""
        plan = RefactorPlan(
            id="test_plan",
            source_file=sample_test_file.metadata.path,
            action=RefactorAction.SPLIT_BY_CONCERN,
            reason="Test",
            description="Test"
        )
        
        service._plan_split_by_concern(plan, sample_test_file)
        
        # Should create 2-3 split files
        assert len(plan.operations) >= 2
        assert len(plan.operations) <= 3
    
    def test_plan_extract_shared(self, service, sample_test_file):
        """Test planning extract shared"""
        plan = RefactorPlan(
            id="test_plan",
            source_file=sample_test_file.metadata.path,
            action=RefactorAction.EXTRACT_SHARED,
            reason="Test",
            description="Test"
        )
        
        service._plan_extract_shared(plan, sample_test_file)
        
        # Should create utils file and modify source
        assert len(plan.operations) == 2
        assert any(op.action == 'create' for op in plan.operations)
        assert any(op.action == 'modify' for op in plan.operations)
    
    def test_calculate_confidence_high(self, service, sample_test_file):
        """Test calculating high confidence"""
        # File has 8 categories > 8
        confidence = service._calculate_confidence(
            sample_test_file,
            RefactorAction.SPLIT_BY_CATEGORY
        )
        
        assert confidence >= 0.8
    
    def test_calculate_confidence_medium(self, service, tmp_path):
        """Test calculating medium confidence"""
        path = tmp_path / "test.spec.ts"
        path.write_text("test")
        
        metadata = FileMetadata(
            path=path, relative_path=Path("test.spec.ts"), module="test",
            size_bytes=1000, total_lines=300, code_lines=250,
            comment_lines=25, blank_lines=25, last_modified=datetime.now()
        )
        
        test_file = TestFile(
            metadata=metadata,
            categories=[f"Cat{i}" for i in range(5)]
        )
        
        confidence = service._calculate_confidence(
            test_file,
            RefactorAction.SPLIT_BY_CATEGORY
        )
        
        assert 0.5 <= confidence < 0.8
    
    def test_calculate_priority_high(self, service, tmp_path):
        """Test calculating high priority"""
        path = tmp_path / "test.spec.ts"
        path.write_text("test")
        
        metadata = FileMetadata(
            path=path, relative_path=Path("test.spec.ts"), module="test",
            size_bytes=5000, total_lines=600, code_lines=500,
            comment_lines=50, blank_lines=50, last_modified=datetime.now()
        )
        
        test_file = TestFile(
            metadata=metadata,
            categories=[f"Cat{i}" for i in range(12)]
        )
        test_file.complexity = Complexity(
            score=85.0,
            level=ComplexityLevel.COMPLEX,
            factors={}
        )
        
        priority = service._calculate_priority(test_file)
        assert priority >= 4
    
    def test_calculate_priority_medium(self, service, sample_test_file):
        """Test calculating medium priority"""
        priority = service._calculate_priority(sample_test_file)
        assert 3 <= priority <= 4
    
    def test_calculate_priority_low(self, service, tmp_path):
        """Test calculating low priority"""
        path = tmp_path / "test.spec.ts"
        path.write_text("test")
        
        metadata = FileMetadata(
            path=path, relative_path=Path("test.spec.ts"), module="test",
            size_bytes=500, total_lines=100, code_lines=80,
            comment_lines=10, blank_lines=10, last_modified=datetime.now()
        )
        
        test_file = TestFile(
            metadata=metadata,
            categories=["Tests"]
        )
        
        priority = service._calculate_priority(test_file)
        assert priority == 3  # Default priority
    
    def test_create_plan_for_file(self, service, sample_test_file):
        """Test creating complete plan for file"""
        plan = service._create_plan_for_file(sample_test_file)
        
        assert isinstance(plan, RefactorPlan)
        assert plan.source_file == sample_test_file.metadata.path
        assert plan.action in [
            RefactorAction.SPLIT_BY_CATEGORY,
            RefactorAction.SPLIT_BY_CONCERN,
            RefactorAction.EXTRACT_SHARED,
            RefactorAction.KEEP_AS_IS
        ]
        assert len(plan.operations) > 0
        assert 0 <= plan.confidence <= 1
        assert 1 <= plan.priority <= 5
    
    def test_plan_marked_ready(self, service, sample_test_file):
        """Test plan is marked as ready"""
        plan = service._create_plan_for_file(sample_test_file)
        
        assert plan.status.value == 'ready'
        assert plan.estimated_impact is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
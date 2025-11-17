# =============================================================================
# tests/unit/domain/test_test_file.py
# =============================================================================
"""Unit tests for TestFile entity"""

import pytest
from pathlib import Path
from datetime import datetime

from src.domain.entities.test_file import TestFile
from src.domain.value_objects.file_metadata import FileMetadata
from src.domain.value_objects.complexity import Complexity, ComplexityLevel


class TestTestFileEntity:
    """Test TestFile entity"""
    
    @pytest.fixture
    def sample_metadata(self):
        """Create sample file metadata"""
        return FileMetadata(
            path=Path("/test/file.spec.ts"),
            relative_path=Path("src/file.spec.ts"),
            module="test-module",
            size_bytes=1024,
            total_lines=100,
            code_lines=80,
            comment_lines=10,
            blank_lines=10,
            last_modified=datetime.now()
        )
    
    @pytest.fixture
    def sample_test_file(self, sample_metadata):
        """Create sample test file"""
        return TestFile(
            metadata=sample_metadata,
            imports=["import { Test } from '@nestjs/testing'"],
            mock_data=[{"name": "mockUser", "type": "object"}],
            categories=["User Tests", "Auth Tests"],
            test_cases=["should create user", "should login"],
            setup_hooks=["beforeEach"]
        )
    
    def test_create_test_file(self, sample_test_file):
        """Test creating test file"""
        assert sample_test_file.metadata.module == "test-module"
        assert len(sample_test_file.imports) == 1
        assert len(sample_test_file.categories) == 2
        assert len(sample_test_file.test_cases) == 2
    
    def test_calculate_complexity(self, sample_test_file):
        """Test calculating complexity"""
        complexity = sample_test_file.calculate_complexity()
        
        assert isinstance(complexity, Complexity)
        assert complexity.score >= 0
        assert complexity.level in [
            ComplexityLevel.SIMPLE,
            ComplexityLevel.MEDIUM,
            ComplexityLevel.COMPLEX
        ]
    
    def test_needs_refactoring_simple_file(self, sample_metadata):
        """Test needs_refactoring for simple file"""
        test_file = TestFile(
            metadata=sample_metadata,
            categories=["Tests"],
            test_cases=["test1", "test2"]
        )
        
        assert not test_file.needs_refactoring()
    
    def test_needs_refactoring_complex_file(self, sample_metadata):
        """Test needs_refactoring for complex file"""
        # Create metadata with many lines
        complex_metadata = FileMetadata(
            path=sample_metadata.path,
            relative_path=sample_metadata.relative_path,
            module=sample_metadata.module,
            size_bytes=10240,
            total_lines=500,  # Too many lines
            code_lines=400,
            comment_lines=50,
            blank_lines=50,
            last_modified=datetime.now()
        )
        
        test_file = TestFile(
            metadata=complex_metadata,
            categories=[f"Cat{i}" for i in range(10)],  # Too many categories
            test_cases=[f"test{i}" for i in range(30)]  # Too many tests
        )
        
        assert test_file.needs_refactoring()
    
    def test_get_refactoring_reason(self, sample_metadata):
        """Test getting refactoring reason"""
        complex_metadata = FileMetadata(
            path=sample_metadata.path,
            relative_path=sample_metadata.relative_path,
            module=sample_metadata.module,
            size_bytes=10240,
            total_lines=500,
            code_lines=400,
            comment_lines=50,
            blank_lines=50,
            last_modified=datetime.now()
        )
        
        test_file = TestFile(
            metadata=complex_metadata,
            categories=[f"Cat{i}" for i in range(10)],
            test_cases=[f"test{i}" for i in range(30)]
        )
        
        reason = test_file.get_refactoring_reason()
        
        assert "lines" in reason or "categories" in reason or "test cases" in reason
    
    def test_recommend_action_split_by_category(self, sample_metadata):
        """Test action recommendation for many categories"""
        test_file = TestFile(
            metadata=sample_metadata,
            categories=[f"Cat{i}" for i in range(10)],  # Many categories
            test_cases=["test1", "test2"]
        )
        
        action = test_file.recommend_action()
        assert action == "split_by_category"
    
    def test_recommend_action_split_by_concern(self, sample_metadata):
        """Test action recommendation for many tests"""
        test_file = TestFile(
            metadata=sample_metadata,
            categories=["Tests"],
            test_cases=[f"test{i}" for i in range(25)]  # Many tests
        )
        
        action = test_file.recommend_action()
        assert action == "split_by_concern"
    
    def test_to_dict(self, sample_test_file):
        """Test converting to dictionary"""
        data = sample_test_file.to_dict()
        
        assert 'path' in data
        assert 'categories' in data
        assert 'test_count' in data
        assert 'needs_refactoring' in data
        assert 'recommended_action' in data
# =============================================================================
# tests/unit/application/services/test_analysis_service.py
# =============================================================================
"""Unit tests for AnalysisService"""

import pytest
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime

from src.application.services.analysis_service import AnalysisService
from src.domain.entities.test_file import TestFile
from src.domain.value_objects.file_metadata import FileMetadata
from src.domain.value_objects.complexity import Complexity, ComplexityLevel
from src.infrastructure.parsers.base_parser import ParseResult


class TestAnalysisService:
    """Test AnalysisService"""
    
    @pytest.fixture
    def mock_scanner(self):
        """Create mock file scanner"""
        scanner = Mock()
        scanner.scan.return_value = []
        return scanner
    
    @pytest.fixture
    def mock_parser(self):
        """Create mock TypeScript parser"""
        parser = Mock()
        
        # Create sample parse result
        parse_result = ParseResult(
            imports=["import { Test } from '@nestjs/testing'"],
            mock_data=[{"name": "mockUser", "type": "object"}],
            categories=["User Tests"],
            test_cases=["should create user"],
            setup_hooks=["beforeEach"],
            complexity_metrics={"cyclomatic_complexity": 10},
            raw_data={}
        )
        parser.parse.return_value = parse_result
        return parser
    
    @pytest.fixture
    def mock_complexity_analyzer(self):
        """Create mock complexity analyzer"""
        analyzer = Mock()
        complexity = Complexity(
            score=45.0,
            level=ComplexityLevel.MEDIUM,
            factors={"lines": 20.0}
        )
        analyzer.analyze.return_value = complexity
        return analyzer
    
    @pytest.fixture
    def mock_quality_analyzer(self):
        """Create mock quality analyzer"""
        analyzer = Mock()
        analyzer.detect_smells.return_value = ["long_test_file"]
        return analyzer
    
    @pytest.fixture
    def mock_repository(self):
        """Create mock repository"""
        repo = Mock()
        repo.save_all.return_value = None
        return repo
    
    @pytest.fixture
    def service(self, mock_scanner, mock_parser, mock_complexity_analyzer,
                mock_quality_analyzer, mock_repository):
        """Create analysis service with mocked dependencies"""
        return AnalysisService(
            mock_scanner,
            mock_parser,
            mock_complexity_analyzer,
            mock_quality_analyzer,
            mock_repository
        )
    
    @pytest.fixture
    def temp_test_file(self, tmp_path):
        """Create temporary test file"""
        test_file = tmp_path / "test.spec.ts"
        test_file.write_text("""
import { Test } from '@nestjs/testing';

const mockUser = { id: 1 };

describe('Tests', () => {
  it('should work', () => {
    expect(true).toBe(true);
  });
});
""")
        return test_file
    
    def test_analyze_directory_empty(self, service, tmp_path, mock_scanner):
        """Test analyzing empty directory"""
        mock_scanner.scan.return_value = []
        
        result = service.analyze_directory(tmp_path)
        
        assert result.total_files == 0
        assert result.analyzed_files == 0
        assert result.candidates_for_refactoring == 0
    
    def test_analyze_directory_with_files(self, service, tmp_path, 
                                         mock_scanner, temp_test_file):
        """Test analyzing directory with files"""
        mock_scanner.scan.return_value = [temp_test_file]
        
        result = service.analyze_directory(tmp_path)
        
        assert result.total_files == 1
        assert result.analyzed_files == 1
        assert result.execution_time >= 0
    
    def test_analyze_file_success(self, service, temp_test_file):
        """Test analyzing single file successfully"""
        test_file = service._analyze_file(temp_test_file)
        
        assert isinstance(test_file, TestFile)
        assert test_file.metadata.path == temp_test_file
        assert len(test_file.imports) > 0
    
    def test_calculate_statistics_empty(self, service):
        """Test calculating statistics with empty list"""
        stats = service._calculate_statistics([])
        
        assert stats == {}
    
    def test_calculate_statistics(self, service, tmp_path):
        """Test calculating statistics"""
        # Create test files
        files = []
        for i in range(3):
            metadata = FileMetadata(
                path=tmp_path / f"test{i}.spec.ts",
                relative_path=Path(f"test{i}.spec.ts"),
                module="test",
                size_bytes=1000,
                total_lines=100 + (i * 50),
                code_lines=80,
                comment_lines=10,
                blank_lines=10,
                last_modified=datetime.now()
            )
            
            test_file = TestFile(
                metadata=metadata,
                categories=["Tests"],
                test_cases=[f"test{j}" for j in range(5)]
            )
            test_file.calculate_complexity()
            files.append(test_file)
        
        stats = service._calculate_statistics(files)
        
        assert 'total_files' in stats
        assert 'total_lines' in stats
        assert 'complexity_distribution' in stats
        assert stats['total_files'] == 3
    
    def test_count_code_lines(self, service):
        """Test counting code lines"""
        content = """
// Comment
const x = 1;
const y = 2;

// Another comment
function test() {
  return true;
}
"""
        count = service._count_code_lines(content)
        assert count > 0
    
    def test_count_comment_lines(self, service):
        """Test counting comment lines"""
        content = """
// Comment 1
const x = 1;
// Comment 2
const y = 2;
"""
        count = service._count_comment_lines(content)
        assert count == 2
    
    def test_count_blank_lines(self, service):
        """Test counting blank lines"""
        content = """line1

line2

line3"""
        count = service._count_blank_lines(content)
        assert count == 2
    
    def test_analyze_directory_saves_to_repository(self, service, tmp_path,
                                                   mock_scanner, mock_repository,
                                                   temp_test_file):
        """Test that analysis saves results to repository"""
        mock_scanner.scan.return_value = [temp_test_file]
        
        service.analyze_directory(tmp_path)
        
        mock_repository.save_all.assert_called_once()
        args = mock_repository.save_all.call_args[0][0]
        assert len(args) == 1
        assert isinstance(args[0], TestFile)
    
    def test_analyze_directory_timing(self, service, tmp_path, mock_scanner):
        """Test that analysis includes execution timing"""
        mock_scanner.scan.return_value = []
        
        result = service.analyze_directory(tmp_path)
        
        assert result.execution_time >= 0
        assert isinstance(result.timestamp, datetime)
    
    def test_analyze_file_with_quality(self, service, temp_test_file):
        """Test analyzing file includes quality calculation"""
        test_file = service._analyze_file(temp_test_file)
        
        assert test_file.quality is not None
        assert 0 <= test_file.quality.score <= 100
    
    def test_analyze_file_with_complexity(self, service, temp_test_file):
        """Test analyzing file includes complexity calculation"""
        test_file = service._analyze_file(temp_test_file)
        
        assert test_file.complexity is not None
        assert 0 <= test_file.complexity.score <= 100


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
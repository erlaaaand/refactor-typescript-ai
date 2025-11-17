# =============================================================================
# tests/integration/test_analysis_workflow.py
# =============================================================================
"""Integration tests for analysis workflow"""

import pytest
from pathlib import Path
import tempfile
import shutil

from src.application.use_cases.analyze_test_files import (
    AnalyzeTestFilesUseCase,
    AnalyzeTestFilesRequest
)
from src.application.services.analysis_service import AnalysisService
from src.infrastructure.scanners.file_scanner import FileScanner
from src.infrastructure.parsers.typescript_parser import TypeScriptParser
from src.infrastructure.analyzers.complexity_analyzer import ComplexityAnalyzer
from src.infrastructure.analyzers.quality_analyzer import QualityAnalyzer
from src.infrastructure.persistence.file_storage import FileTestFileRepository


class TestAnalysisWorkflow:
    """Test complete analysis workflow"""
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory with test files"""
        temp = Path(tempfile.mkdtemp())
        
        # Create sample test file
        test_dir = temp / "src" / "users" / "__tests__"
        test_dir.mkdir(parents=True)
        
        test_file = test_dir / "user.service.spec.ts"
        test_file.write_text("""
import { Test } from '@nestjs/testing';
import { UserService } from '../user.service';

describe('UserService', () => {
  let service: UserService;
  
  beforeEach(() => {
    service = new UserService();
  });
  
  describe('create', () => {
    it('should create a user', () => {
      const result = service.create({ name: 'Test' });
      expect(result).toBeDefined();
    });
  });
  
  describe('findAll', () => {
    it('should return all users', () => {
      const users = service.findAll();
      expect(users).toBeInstanceOf(Array);
    });
  });
});
""")
        
        yield temp
        
        # Cleanup
        shutil.rmtree(temp)
    
    def test_complete_analysis_workflow(self, temp_dir):
        """Test complete analysis from scan to result"""
        
        # Setup dependencies
        scanner = FileScanner(max_workers=1)
        parser = TypeScriptParser()
        complexity_analyzer = ComplexityAnalyzer()
        quality_analyzer = QualityAnalyzer()
        repository = FileTestFileRepository(temp_dir / "output")
        
        service = AnalysisService(
            scanner, parser, complexity_analyzer,
            quality_analyzer, repository
        )
        
        use_case = AnalyzeTestFilesUseCase(service)
        
        # Execute
        request = AnalyzeTestFilesRequest(
            root_directory=temp_dir / "src",
            max_workers=1,
            verbose=False
        )
        
        result = use_case.execute(request)
        
        # Assertions
        assert result.total_files == 1
        assert result.analyzed_files == 1
        assert result.execution_time > 0
        assert 'complexity_distribution' in result.statistics
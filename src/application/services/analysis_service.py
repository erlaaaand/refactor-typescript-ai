# =============================================================================
# src/application/services/analysis_service.py
# =============================================================================
"""Analysis Service - Orchestrates file analysis"""

from pathlib import Path
from typing import List, Dict
import time
from datetime import datetime

from ...domain.entities.test_file import TestFile
from ...domain.repositories.test_file_repository import TestFileRepository
from ...infrastructure.scanners.file_scanner import FileScanner
from ...infrastructure.parsers.typescript_parser import TypeScriptParser
from ...infrastructure.analyzers.complexity_analyzer import ComplexityAnalyzer
from ...infrastructure.analyzers.quality_analyzer import QualityAnalyzer
from ..dto.analysis_result import AnalysisResult


class AnalysisService:
    """Service for analyzing test files"""
    
    def __init__(
        self,
        scanner: FileScanner,
        parser: TypeScriptParser,
        complexity_analyzer: ComplexityAnalyzer,
        quality_analyzer: QualityAnalyzer,
        repository: TestFileRepository
    ):
        self.scanner = scanner
        self.parser = parser
        self.complexity_analyzer = complexity_analyzer
        self.quality_analyzer = quality_analyzer
        self.repository = repository
    
    def analyze_directory(self, root_dir: Path) -> AnalysisResult:
        """Analyze all test files in directory"""
        start_time = time.time()
        
        # Scan for files
        file_paths = self.scanner.scan(root_dir)
        
        # Analyze each file
        test_files = []
        for file_path in file_paths:
            test_file = self._analyze_file(file_path)
            if test_file:
                test_files.append(test_file)
        
        # Save to repository
        self.repository.save_all(test_files)
        
        # Calculate statistics
        statistics = self._calculate_statistics(test_files)
        candidates = [tf for tf in test_files if tf.needs_refactoring()]
        
        execution_time = time.time() - start_time
        
        return AnalysisResult(
            total_files=len(file_paths),
            analyzed_files=len(test_files),
            candidates_for_refactoring=len(candidates),
            statistics=statistics,
            execution_time=execution_time,
            timestamp=datetime.now()
        )
    
    def _analyze_file(self, file_path: Path) -> TestFile:
        """Analyze a single test file"""
        # Read file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse
        parse_result = self.parser.parse(content)
        
        # Create metadata
        from ...domain.value_objects.file_metadata import FileMetadata
        stat = file_path.stat()
        
        metadata = FileMetadata(
            path=file_path,
            relative_path=file_path,  # This should be relative to root
            module=file_path.parent.parent.name,
            size_bytes=stat.st_size,
            total_lines=len(content.split('\n')),
            code_lines=self._count_code_lines(content),
            comment_lines=self._count_comment_lines(content),
            blank_lines=self._count_blank_lines(content),
            last_modified=datetime.fromtimestamp(stat.st_mtime)
        )
        
        # Create entity
        test_file = TestFile(
            metadata=metadata,
            imports=parse_result.imports,
            mock_data=parse_result.mock_data,
            categories=parse_result.categories,
            test_cases=parse_result.test_cases,
            setup_hooks=parse_result.setup_hooks
        )
        
        # Calculate metrics
        test_file.calculate_complexity()
        
        # Calculate quality
        cyclomatic = parse_result.complexity_metrics.get('cyclomatic_complexity', 0)
        code_smells = self.quality_analyzer.detect_smells(test_file)
        test_file.calculate_quality(cyclomatic, len(code_smells))
        
        return test_file
    
    def _count_code_lines(self, content: str) -> int:
        """Count actual code lines"""
        lines = content.split('\n')
        return sum(
            1 for line in lines
            if line.strip() and not line.strip().startswith('//')
        )
    
    def _count_comment_lines(self, content: str) -> int:
        """Count comment lines"""
        lines = content.split('\n')
        return sum(1 for line in lines if line.strip().startswith('//'))
    
    def _count_blank_lines(self, content: str) -> int:
        """Count blank lines"""
        lines = content.split('\n')
        return sum(1 for line in lines if not line.strip())
    
    def _calculate_statistics(self, test_files: List[TestFile]) -> Dict:
        """Calculate aggregate statistics"""
        if not test_files:
            return {}
        
        total_lines = sum(tf.metadata.total_lines for tf in test_files)
        total_tests = sum(len(tf.test_cases) for tf in test_files)
        
        complexity_distribution = {
            'simple': sum(1 for tf in test_files if tf.complexity.level.value == 'simple'),
            'medium': sum(1 for tf in test_files if tf.complexity.level.value == 'medium'),
            'complex': sum(1 for tf in test_files if tf.complexity.level.value == 'complex')
        }
        
        quality_distribution = {
            'excellent': sum(1 for tf in test_files if tf.quality and tf.quality.score >= 80),
            'good': sum(1 for tf in test_files if tf.quality and 60 <= tf.quality.score < 80),
            'fair': sum(1 for tf in test_files if tf.quality and 40 <= tf.quality.score < 60),
            'poor': sum(1 for tf in test_files if tf.quality and tf.quality.score < 40)
        }
        
        return {
            'total_files': len(test_files),
            'total_lines': total_lines,
            'total_tests': total_tests,
            'avg_lines': total_lines // len(test_files),
            'avg_tests': total_tests // len(test_files),
            'complexity_distribution': complexity_distribution,
            'quality_distribution': quality_distribution
        }
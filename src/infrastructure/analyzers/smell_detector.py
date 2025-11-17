# =============================================================================
# src/infrastructure/analyzers/smell_detector.py
# =============================================================================
"""Code Smell Detector - Identifies anti-patterns and code smells"""

from typing import List, Dict
from dataclasses import dataclass
from ...domain.entities.test_file import TestFile


@dataclass
class CodeSmell:
    """Represents a detected code smell"""
    type: str
    severity: str  # 'low', 'medium', 'high'
    description: str
    location: str
    suggestion: str


class SmellDetector:
    """Detects code smells in test files"""
    
    def __init__(self):
        self.severity_thresholds = {
            'long_file': {'high': 500, 'medium': 300},
            'many_categories': {'high': 10, 'medium': 6},
            'many_tests': {'high': 30, 'medium': 20},
            'many_mocks': {'high': 10, 'medium': 5}
        }
    
    def detect(self, test_file: TestFile) -> List[CodeSmell]:
        """Detect all code smells in test file"""
        smells = []
        
        smells.extend(self._check_file_length(test_file))
        smells.extend(self._check_categories(test_file))
        smells.extend(self._check_test_count(test_file))
        smells.extend(self._check_mocks(test_file))
        smells.extend(self._check_structure(test_file))
        smells.extend(self._check_setup_hooks(test_file))
        
        return smells
    
    def _check_file_length(self, test_file: TestFile) -> List[CodeSmell]:
        """Check for overly long test files"""
        lines = test_file.metadata.total_lines
        
        if lines > self.severity_thresholds['long_file']['high']:
            return [CodeSmell(
                type='long_test_file',
                severity='high',
                description=f'Test file is too long ({lines} lines)',
                location=str(test_file.metadata.path),
                suggestion='Split into multiple files by category or concern'
            )]
        elif lines > self.severity_thresholds['long_file']['medium']:
            return [CodeSmell(
                type='long_test_file',
                severity='medium',
                description=f'Test file is getting long ({lines} lines)',
                location=str(test_file.metadata.path),
                suggestion='Consider splitting if adding more tests'
            )]
        
        return []
    
    def _check_categories(self, test_file: TestFile) -> List[CodeSmell]:
        """Check for too many test categories"""
        count = len(test_file.categories)
        
        if count > self.severity_thresholds['many_categories']['high']:
            return [CodeSmell(
                type='too_many_categories',
                severity='high',
                description=f'Too many test categories ({count})',
                location=str(test_file.metadata.path),
                suggestion='Split by category into separate files'
            )]
        elif count > self.severity_thresholds['many_categories']['medium']:
            return [CodeSmell(
                type='too_many_categories',
                severity='medium',
                description=f'Many test categories ({count})',
                location=str(test_file.metadata.path),
                suggestion='Consider organizing into fewer categories'
            )]
        elif count == 0 and len(test_file.test_cases) > 10:
            return [CodeSmell(
                type='no_categories',
                severity='medium',
                description='Tests not organized into categories',
                location=str(test_file.metadata.path),
                suggestion='Group related tests using describe blocks'
            )]
        
        return []
    
    def _check_test_count(self, test_file: TestFile) -> List[CodeSmell]:
        """Check for too many test cases"""
        count = len(test_file.test_cases)
        
        if count > self.severity_thresholds['many_tests']['high']:
            return [CodeSmell(
                type='too_many_tests',
                severity='high',
                description=f'Too many test cases ({count})',
                location=str(test_file.metadata.path),
                suggestion='Split by testing concern or feature'
            )]
        elif count > self.severity_thresholds['many_tests']['medium']:
            return [CodeSmell(
                type='too_many_tests',
                severity='medium',
                description=f'Many test cases ({count})',
                location=str(test_file.metadata.path),
                suggestion='Consider splitting large test suites'
            )]
        
        return []
    
    def _check_mocks(self, test_file: TestFile) -> List[CodeSmell]:
        """Check for mock-related smells"""
        count = len(test_file.mock_data)
        smells = []
        
        if count > self.severity_thresholds['many_mocks']['high']:
            smells.append(CodeSmell(
                type='mock_overload',
                severity='high',
                description=f'Too many mock definitions ({count})',
                location=str(test_file.metadata.path),
                suggestion='Extract shared mocks to test utilities'
            ))
        elif count > self.severity_thresholds['many_mocks']['medium']:
            smells.append(CodeSmell(
                type='mock_overload',
                severity='medium',
                description=f'Many mock definitions ({count})',
                location=str(test_file.metadata.path),
                suggestion='Consider extracting common mocks'
            ))
        
        if count > 0 and not test_file.setup_hooks:
            smells.append(CodeSmell(
                type='no_setup_with_mocks',
                severity='low',
                description='Mocks defined but no setup hooks',
                location=str(test_file.metadata.path),
                suggestion='Use beforeEach/beforeAll for mock setup'
            ))
        
        return smells
    
    def _check_structure(self, test_file: TestFile) -> List[CodeSmell]:
        """Check for structural issues"""
        smells = []
        
        if not test_file.categories and len(test_file.test_cases) > 5:
            smells.append(CodeSmell(
                type='flat_structure',
                severity='low',
                description='Tests lack hierarchical structure',
                location=str(test_file.metadata.path),
                suggestion='Group related tests in describe blocks'
            ))
        
        return smells
    
    def _check_setup_hooks(self, test_file: TestFile) -> List[CodeSmell]:
        """Check for setup/teardown hook issues"""
        smells = []
        
        if len(test_file.setup_hooks) > 3:
            smells.append(CodeSmell(
                type='too_many_hooks',
                severity='medium',
                description=f'Too many setup hooks ({len(test_file.setup_hooks)})',
                location=str(test_file.metadata.path),
                suggestion='Simplify test setup/teardown logic'
            ))
        
        return smells
    
    def get_summary(self, smells: List[CodeSmell]) -> Dict[str, int]:
        """Get summary of detected smells by severity"""
        return {
            'total': len(smells),
            'high': sum(1 for s in smells if s.severity == 'high'),
            'medium': sum(1 for s in smells if s.severity == 'medium'),
            'low': sum(1 for s in smells if s.severity == 'low')
        }
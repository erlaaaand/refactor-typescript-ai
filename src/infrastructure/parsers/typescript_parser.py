# =============================================================================
# src/infrastructure/parsers/typescript_parser.py
# =============================================================================
"""Main TypeScript Parser - Orchestrates all sub-parsers"""

from typing import List
from .base_parser import BaseParser, ParseResult
from .import_parser import ImportParser
from .mock_parser import MockParser
from .test_structure_parser import TestStructureParser


class TypeScriptParser(BaseParser):
    """Main parser for TypeScript test files"""
    
    def __init__(self):
        self.import_parser = ImportParser()
        self.mock_parser = MockParser()
        self.structure_parser = TestStructureParser()
    
    def can_parse(self, file_path: str) -> bool:
        """Check if file is a TypeScript test file"""
        return file_path.endswith(('.spec.ts', '.test.ts', '.spec.tsx', '.test.tsx'))
    
    def parse(self, content: str) -> ParseResult:
        """Parse TypeScript test file"""
        lines = content.split('\n')
        
        # Parse imports
        import_statements = self.import_parser.parse_imports(content)
        imports = [stmt.raw for stmt in import_statements]
        
        # Parse mocks
        mock_variables = self.mock_parser.parse_mocks(lines)
        mock_data = [
            {
                'name': mock.name,
                'content': mock.content,
                'type': mock.mock_type,
                'complexity': mock.complexity,
                'start_line': mock.start_line,
                'end_line': mock.end_line
            }
            for mock in mock_variables
        ]
        
        # Parse structure
        blocks = self.structure_parser.parse_structure(lines)
        categories = self.structure_parser.extract_categories(blocks)
        test_cases = self.structure_parser.extract_test_cases(blocks)
        
        # Extract hooks
        setup_hooks = [
            block.name for block in blocks
            if block.type.name in ['BEFORE_EACH', 'AFTER_EACH', 'BEFORE_ALL', 'AFTER_ALL']
        ]
        
        # Calculate complexity metrics
        complexity_metrics = self._calculate_complexity(content, blocks)
        
        return ParseResult(
            imports=imports,
            mock_data=mock_data,
            categories=categories,
            test_cases=test_cases,
            setup_hooks=setup_hooks,
            complexity_metrics=complexity_metrics,
            raw_data={
                'import_statements': import_statements,
                'mock_variables': mock_variables,
                'blocks': blocks
            }
        )
    
    def _calculate_complexity(self, content: str, blocks: List) -> dict:
        """Calculate basic complexity metrics"""
        return {
            'cyclomatic_complexity': self._calculate_cyclomatic(content),
            'max_nesting_depth': self._calculate_nesting_depth(blocks),
            'total_blocks': len(blocks)
        }
    
    def _calculate_cyclomatic(self, content: str) -> int:
        """Calculate cyclomatic complexity"""
        return (
            content.count('if ') +
            content.count('else ') +
            content.count('switch ') +
            content.count('for ') +
            content.count('while ') +
            content.count('&&') +
            content.count('||') +
            1
        )
    
    def _calculate_nesting_depth(self, blocks: List) -> int:
        """Calculate maximum nesting depth"""
        def get_depth(block, current_depth=0):
            if not block.children:
                return current_depth
            return max(get_depth(child, current_depth + 1) for child in block.children)
        
        if not blocks:
            return 0
        
        return max(get_depth(block) for block in blocks)
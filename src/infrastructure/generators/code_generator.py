# =============================================================================
# src/infrastructure/generators/code_generator.py
# =============================================================================
"""Code Generator - Generates TypeScript test code"""

from typing import List, Dict
from pathlib import Path


class CodeGenerator:
    """Generates TypeScript test file code"""
    
    def __init__(self):
        self.indent = "  "
    
    def generate_test_file(self, 
                          imports: List[str],
                          mocks: List[Dict],
                          describes: List[Dict]) -> str:
        """Generate complete test file"""
        
        sections = []
        
        # Imports
        if imports:
            sections.append(self._generate_imports(imports))
        
        # Mocks
        if mocks:
            sections.append(self._generate_mocks(mocks))
        
        # Test blocks
        for describe in describes:
            sections.append(self._generate_describe_block(describe))
        
        return "\n\n".join(sections) + "\n"
    
    def _generate_imports(self, imports: List[str]) -> str:
        """Generate import statements"""
        return "\n".join(imports)
    
    def _generate_mocks(self, mocks: List[Dict]) -> str:
        """Generate mock data declarations"""
        lines = []
        
        for mock in mocks:
            name = mock.get('name', 'mockData')
            content = mock.get('content', '{}')
            
            lines.append(f"const {name} = {content};")
        
        return "\n".join(lines)
    
    def _generate_describe_block(self, describe: Dict, level: int = 0) -> str:
        """Generate describe block"""
        indent = self.indent * level
        name = describe.get('name', 'Test Suite')
        
        lines = [f"{indent}describe('{name}', () => {{"]
        
        # Setup hooks
        if describe.get('beforeEach'):
            lines.append(f"{indent}{self.indent}beforeEach(() => {{")
            lines.append(f"{indent}{self.indent}{self.indent}// Setup")
            lines.append(f"{indent}{self.indent}}});")
            lines.append("")
        
        # Test cases
        for test in describe.get('tests', []):
            lines.append(self._generate_test_case(test, level + 1))
            lines.append("")
        
        # Nested describes
        for nested in describe.get('nested', []):
            lines.append(self._generate_describe_block(nested, level + 1))
            lines.append("")
        
        lines.append(f"{indent}}});")
        
        return "\n".join(lines)
    
    def _generate_test_case(self, test: Dict, level: int = 0) -> str:
        """Generate test case (it block)"""
        indent = self.indent * level
        name = test.get('name', 'should work')
        is_async = test.get('async', False)
        
        async_keyword = "async " if is_async else ""
        
        lines = [f"{indent}it('{name}', {async_keyword}() => {{"]
        
        # Test body
        body = test.get('body', [])
        if isinstance(body, str):
            body = [body]
        
        for line in body:
            lines.append(f"{indent}{self.indent}{line}")
        
        # Default assertion if no body
        if not body:
            lines.append(f"{indent}{self.indent}expect(true).toBe(true);")
        
        lines.append(f"{indent}}});")
        
        return "\n".join(lines)
    
    def generate_split_file(self, original_file: Path, 
                           category: str,
                           imports: List[str],
                           mocks: List[Dict],
                           tests: List[Dict]) -> str:
        """Generate a split test file for a specific category"""
        
        describe = {
            'name': category,
            'tests': tests
        }
        
        return self.generate_test_file(imports, mocks, [describe])
    
    def generate_utils_file(self, mocks: List[Dict], 
                           helpers: List[Dict]) -> str:
        """Generate test utilities file"""
        
        sections = []
        
        # Mocks as exports
        if mocks:
            sections.append("// Mock Data")
            for mock in mocks:
                name = mock.get('name', 'mockData')
                content = mock.get('content', '{}')
                sections.append(f"export const {name} = {content};")
        
        # Helper functions
        if helpers:
            sections.append("\n// Helper Functions")
            for helper in helpers:
                sections.append(self._generate_helper(helper))
        
        return "\n\n".join(sections) + "\n"
    
    def _generate_helper(self, helper: Dict) -> str:
        """Generate helper function"""
        name = helper.get('name', 'helperFunction')
        params = helper.get('params', [])
        body = helper.get('body', 'return null;')
        
        params_str = ", ".join(params)
        
        return f"""export function {name}({params_str}) {{
  {body}
}}"""
    
    def generate_file_header(self, description: str = "") -> str:
        """Generate file header comment"""
        return f"""/**
 * {description}
 * Auto-generated by Test Refactor AI
 * Generated at: {self._get_timestamp()}
 */
"""
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
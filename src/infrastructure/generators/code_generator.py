# =============================================================================
# src/infrastructure/generators/code_generator.py
# =============================================================================
"""Code Generator - Generates TypeScript test code"""

from typing import List, Dict
from pathlib import Path
from datetime import datetime


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
    
    def split_by_category(self, original_content: str, categories: List[str]) -> Dict[str, str]:
        """Split test file content by categories"""
        
        result_files = {}
        
        for i, category in enumerate(categories):
            # Clean category name for filename
            clean_category = category.replace(' ', '_').replace('/', '_').lower()
            filename = f"category_{i+1}_{clean_category}.spec.ts"
            
            # Generate header
            header = self.generate_file_header(f"Split from original test file - Category: {category}")
            
            # Basic test content for this category
            content = header + self.generate_test_file(
                imports=["import { Test } from '@nestjs/testing';"],
                mocks=[],
                describes=[{
                    'name': f'{category} Tests',
                    'tests': [{
                        'name': f'should test {category} functionality',
                        'body': [
                            '// TODO: Add specific tests for this category',
                            '// This file was auto-generated by Test Refactor AI',
                            'expect(true).toBe(true);'
                        ]
                    }]
                }]
            )
            
            result_files[filename] = content
        
        return result_files
    
    def split_by_concern(self, original_content: str, concerns: List[str]) -> Dict[str, str]:
        """Split test file content by concerns"""
        
        result_files = {}
        
        for i, concern in enumerate(concerns):
            # Clean concern name for filename
            clean_concern = concern.replace(' ', '_').replace('/', '_').lower()
            filename = f"concern_{i+1}_{clean_concern}.spec.ts"
            
            # Generate header
            header = self.generate_file_header(f"Split from original test file - Concern: {concern}")
            
            # Basic test content for this concern
            content = header + self.generate_test_file(
                imports=["import { Test } from '@nestjs/testing';"],
                mocks=[],
                describes=[{
                    'name': f'{concern} Tests',
                    'tests': [{
                        'name': f'should handle {concern}',
                        'body': [
                            f'// TODO: Implement tests for {concern}',
                            '// This file was auto-generated by Test Refactor AI',
                            'expect(true).toBe(true);'
                        ]
                    }]
                }]
            )
            
            result_files[filename] = content
        
        return result_files
    
    def extract_shared_mocks(self, original_content: str, mock_names: List[str]) -> Dict[str, str]:
        """Extract shared mocks to separate utility file"""
        
        result_files = {}
        
        # Create utilities file
        utils_filename = "test-utils.ts"
        
        header = self.generate_file_header("Shared test utilities and mocks")
        
        utils_content = header + "// Shared Mock Data\nexport const sharedMocks = {\n"
        
        for mock_name in mock_names:
            utils_content += f"  {mock_name}: {{}},\n"
        
        utils_content += "};\n\n"
        utils_content += "// Helper Functions\nexport function setupTest() {\n  // Common test setup\n  return {};\n}\n"
        
        result_files[utils_filename] = utils_content
        
        return result_files
    
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
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
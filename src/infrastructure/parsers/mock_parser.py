# =============================================================================
# src/infrastructure/parsers/mock_parser.py
# =============================================================================
"""Mock Data Parser"""

import re
from typing import List, Dict
from dataclasses import dataclass


@dataclass
class MockVariable:
    """Represents a parsed mock variable"""
    name: str
    content: str
    start_line: int
    end_line: int
    mock_type: str
    complexity: int


class MockParser:
    """Parser for mock data and variables"""
    
    CONST_PATTERN = re.compile(r'^\s*const\s+(\w+)\s*[:=]')
    MOCK_PREFIXES = ['mock', 'test', 'fixture', 'stub', 'spy']
    
    def parse_mocks(self, lines: List[str]) -> List[MockVariable]:
        """Extract mock variables from code"""
        mocks = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            match = self.CONST_PATTERN.match(line)
            
            if match:
                var_name = match.group(1)
                
                if self._is_mock_variable(var_name):
                    end_line = self._find_declaration_end(lines, i)
                    content = '\n'.join(lines[i:end_line + 1])
                    
                    mocks.append(MockVariable(
                        name=var_name,
                        content=content,
                        start_line=i,
                        end_line=end_line,
                        mock_type=self._infer_mock_type(content),
                        complexity=self._calculate_mock_complexity(content)
                    ))
                    
                    i = end_line + 1
                    continue
            
            i += 1
        
        return mocks
    
    def _is_mock_variable(self, var_name: str) -> bool:
        """Check if variable name indicates mock data"""
        lower_name = var_name.lower()
        return any(
            lower_name.startswith(prefix) or lower_name.endswith(prefix)
            for prefix in self.MOCK_PREFIXES
        )
    
    def _find_declaration_end(self, lines: List[str], start: int) -> int:
        """Find the end of a variable declaration"""
        brace_count = 0
        paren_count = 0
        bracket_count = 0
        
        for i in range(start, len(lines)):
            line = lines[i]
            
            for char in line:
                if char == '{': brace_count += 1
                elif char == '}': brace_count -= 1
                elif char == '(': paren_count += 1
                elif char == ')': paren_count -= 1
                elif char == '[': bracket_count += 1
                elif char == ']': bracket_count -= 1
            
            if brace_count == 0 and paren_count == 0 and bracket_count == 0:
                if ';' in line:
                    return i
        
        return len(lines) - 1
    
    def _infer_mock_type(self, content: str) -> str:
        """Infer the type of mock data"""
        content_lower = content.lower()
        
        if 'jest.fn' in content_lower:
            return 'function'
        elif '{' in content and '}' in content:
            if 'repository' in content_lower:
                return 'repository'
            return 'object'
        elif '[' in content and ']' in content:
            return 'array'
        else:
            return 'primitive'
    
    def _calculate_mock_complexity(self, content: str) -> int:
        """Calculate complexity score for mock data"""
        complexity = 0
        complexity += content.count('{')
        complexity += content.count('[')
        complexity += len(re.findall(r'\w+:', content))
        complexity += content.count('=>')
        return complexity
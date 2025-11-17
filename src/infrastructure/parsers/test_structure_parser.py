# =============================================================================
# src/infrastructure/parsers/test_structure_parser.py
# =============================================================================
"""Test Structure Parser - Extracts describe/it blocks"""

import re
from typing import List, Dict, Optional
from dataclasses import dataclass, field
from enum import Enum


class BlockType(Enum):
    """Types of test blocks"""
    DESCRIBE = "describe"
    IT = "it"
    BEFORE_EACH = "beforeEach"
    AFTER_EACH = "afterEach"
    BEFORE_ALL = "beforeAll"
    AFTER_ALL = "afterAll"


@dataclass
class TestBlock:
    """Represents a test block (describe/it)"""
    type: BlockType
    name: str
    start_line: int
    end_line: int
    content: str
    children: List['TestBlock'] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)


class TestStructureParser:
    """Parser for test structure (describe/it blocks)"""
    
    DESCRIBE_PATTERN = re.compile(r'describe\([\'"](.+?)[\'"]\s*,')
    IT_PATTERN = re.compile(r'it\([\'"](.+?)[\'"]\s*,')
    HOOK_PATTERN = re.compile(r'(beforeEach|afterEach|beforeAll|afterAll)\(')
    EXPECT_PATTERN = re.compile(r'expect\(')
    
    def parse_structure(self, lines: List[str]) -> List[TestBlock]:
        """Parse test structure into blocks"""
        blocks = []
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            
            if not line or line.startswith('//'):
                i += 1
                continue
            
            # Parse describe blocks
            if 'describe(' in line:
                block = self._parse_describe_block(lines, i)
                if block:
                    blocks.append(block)
                    i = block.end_line + 1
                    continue
            
            # Parse it blocks
            if 'it(' in line:
                block = self._parse_it_block(lines, i)
                if block:
                    blocks.append(block)
                    i = block.end_line + 1
                    continue
            
            # Parse hooks
            if any(hook in line for hook in ['beforeEach', 'afterEach', 'beforeAll', 'afterAll']):
                block = self._parse_hook(lines, i)
                if block:
                    blocks.append(block)
                    i = block.end_line + 1
                    continue
            
            i += 1
        
        return blocks
    
    def _parse_describe_block(self, lines: List[str], start: int) -> Optional[TestBlock]:
        """Parse a describe block"""
        line = lines[start]
        match = self.DESCRIBE_PATTERN.search(line)
        
        if not match:
            return None
        
        name = match.group(1)
        end = self._find_block_end(lines, start)
        content = '\n'.join(lines[start:end + 1])
        
        block = TestBlock(
            type=BlockType.DESCRIBE,
            name=name,
            start_line=start,
            end_line=end,
            content=content,
            metadata={
                'indentation': len(line) - len(line.lstrip()),
                'is_nested': line.startswith(' ')
            }
        )
        
        # Parse children
        i = start + 1
        while i < end:
            child = self._parse_child_block(lines, i)
            if child:
                block.children.append(child)
                i = child.end_line + 1
            else:
                i += 1
        
        return block
    
    def _parse_it_block(self, lines: List[str], start: int) -> Optional[TestBlock]:
        """Parse an it (test case) block"""
        line = lines[start]
        match = self.IT_PATTERN.search(line)
        
        if not match:
            return None
        
        name = match.group(1)
        end = self._find_block_end(lines, start)
        content = '\n'.join(lines[start:end + 1])
        
        # Count expects
        expect_count = len(self.EXPECT_PATTERN.findall(content))
        
        return TestBlock(
            type=BlockType.IT,
            name=name,
            start_line=start,
            end_line=end,
            content=content,
            metadata={
                'expect_count': expect_count,
                'has_async': 'async' in line or 'await' in content,
                'line_count': end - start + 1
            }
        )
    
    def _parse_hook(self, lines: List[str], start: int) -> Optional[TestBlock]:
        """Parse setup/teardown hook"""
        line = lines[start]
        match = self.HOOK_PATTERN.search(line)
        
        if not match:
            return None
        
        hook_type = match.group(1)
        end = self._find_block_end(lines, start)
        
        block_type_map = {
            'beforeEach': BlockType.BEFORE_EACH,
            'afterEach': BlockType.AFTER_EACH,
            'beforeAll': BlockType.BEFORE_ALL,
            'afterAll': BlockType.AFTER_ALL
        }
        
        return TestBlock(
            type=block_type_map[hook_type],
            name=hook_type,
            start_line=start,
            end_line=end,
            content='\n'.join(lines[start:end + 1])
        )
    
    def _parse_child_block(self, lines: List[str], start: int) -> Optional[TestBlock]:
        """Parse a child block within a describe"""
        line = lines[start].strip()
        
        if 'describe(' in line:
            return self._parse_describe_block(lines, start)
        elif 'it(' in line:
            return self._parse_it_block(lines, start)
        elif any(hook in line for hook in ['beforeEach', 'afterEach', 'beforeAll', 'afterAll']):
            return self._parse_hook(lines, start)
        
        return None
    
    def _find_block_end(self, lines: List[str], start: int) -> int:
        """Find the end of a code block by balancing braces"""
        brace_count = 0
        started = False
        
        for i in range(start, len(lines)):
            line = lines[i]
            
            for char in line:
                if char == '{':
                    brace_count += 1
                    started = True
                elif char == '}':
                    brace_count -= 1
            
            if started and brace_count == 0:
                return i
        
        return len(lines) - 1
    
    def extract_categories(self, blocks: List[TestBlock]) -> List[str]:
        """Extract category names from describe blocks"""
        categories = []
        
        for block in blocks:
            if block.type == BlockType.DESCRIBE:
                # Only nested describes are categories
                if block.metadata.get('is_nested', False):
                    categories.append(block.name)
                # Recursively get nested categories
                if block.children:
                    categories.extend(self.extract_categories(block.children))
        
        return categories
    
    def extract_test_cases(self, blocks: List[TestBlock]) -> List[str]:
        """Extract test case names"""
        test_cases = []
        
        for block in blocks:
            if block.type == BlockType.IT:
                test_cases.append(block.name)
            elif block.children:
                test_cases.extend(self.extract_test_cases(block.children))
        
        return test_cases
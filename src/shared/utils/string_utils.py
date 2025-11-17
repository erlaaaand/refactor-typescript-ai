# =============================================================================
# src/shared/utils/string_utils.py
# =============================================================================
"""String utilities for text processing"""

import re
from typing import List


class StringUtils:
    """Utility functions for string operations"""
    
    @staticmethod
    def to_snake_case(text: str) -> str:
        """Convert text to snake_case"""
        # Replace spaces and hyphens with underscores
        text = text.replace(' ', '_').replace('-', '_')
        # Insert underscore before uppercase letters
        text = re.sub('([a-z])([A-Z])', r'\1_\2', text)
        # Convert to lowercase
        return text.lower()
    
    @staticmethod
    def to_camel_case(text: str) -> str:
        """Convert text to camelCase"""
        words = re.split(r'[-_\s]', text)
        if not words:
            return text
        
        return words[0].lower() + ''.join(w.capitalize() for w in words[1:])
    
    @staticmethod
    def to_pascal_case(text: str) -> str:
        """Convert text to PascalCase"""
        words = re.split(r'[-_\s]', text)
        return ''.join(w.capitalize() for w in words)
    
    @staticmethod
    def to_kebab_case(text: str) -> str:
        """Convert text to kebab-case"""
        # Replace spaces and underscores with hyphens
        text = text.replace(' ', '-').replace('_', '-')
        # Insert hyphen before uppercase letters
        text = re.sub('([a-z])([A-Z])', r'\1-\2', text)
        # Convert to lowercase
        return text.lower()
    
    @staticmethod
    def truncate(text: str, max_length: int, suffix: str = "...") -> str:
        """Truncate text to maximum length"""
        if len(text) <= max_length:
            return text
        
        return text[:max_length - len(suffix)] + suffix
    
    @staticmethod
    def strip_comments(code: str) -> str:
        """Remove comments from code"""
        # Remove single-line comments
        code = re.sub(r'//.*$', '', code, flags=re.MULTILINE)
        # Remove multi-line comments
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
        return code
    
    @staticmethod
    def count_words(text: str) -> int:
        """Count words in text"""
        return len(text.split())
    
    @staticmethod
    def extract_quoted_strings(text: str) -> List[str]:
        """Extract all quoted strings from text"""
        # Match both single and double quotes
        pattern = r'["\']([^"\']*)["\']'
        return re.findall(pattern, text)
    
    @staticmethod
    def sanitize_filename(text: str) -> str:
        """Sanitize text for use as filename"""
        # Remove invalid characters
        text = re.sub(r'[<>:"/\\|?*]', '', text)
        # Replace spaces with underscores
        text = text.replace(' ', '_')
        # Remove multiple underscores
        text = re.sub(r'_+', '_', text)
        return text.strip('_')
    
    @staticmethod
    def indent(text: str, spaces: int = 2) -> str:
        """Indent text by specified spaces"""
        indent_str = ' ' * spaces
        return '\n'.join(indent_str + line if line.strip() else line 
                        for line in text.split('\n'))
    
    @staticmethod
    def remove_empty_lines(text: str) -> str:
        """Remove empty lines from text"""
        lines = [line for line in text.split('\n') if line.strip()]
        return '\n'.join(lines)
    
    @staticmethod
    def wrap_text(text: str, width: int = 80) -> str:
        """Wrap text to specified width"""
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            word_length = len(word)
            
            if current_length + word_length + len(current_line) > width:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                    current_length = word_length
                else:
                    lines.append(word)
            else:
                current_line.append(word)
                current_length += word_length
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return '\n'.join(lines)
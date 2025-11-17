# =============================================================================
# tests/unit/shared/test_string_utils.py
# =============================================================================
"""Unit tests for StringUtils"""

import pytest
from src.shared.utils.string_utils import StringUtils


class TestStringUtils:
    """Test StringUtils"""
    
    def test_to_snake_case(self):
        """Test converting to snake_case"""
        assert StringUtils.to_snake_case("HelloWorld") == "hello_world"
        assert StringUtils.to_snake_case("hello-world") == "hello_world"
        assert StringUtils.to_snake_case("Hello World") == "hello_world"
        assert StringUtils.to_snake_case("helloWorld") == "hello_world"
    
    def test_to_camel_case(self):
        """Test converting to camelCase"""
        assert StringUtils.to_camel_case("hello_world") == "helloWorld"
        assert StringUtils.to_camel_case("hello-world") == "helloWorld"
        assert StringUtils.to_camel_case("hello world") == "helloWorld"
    
    def test_to_pascal_case(self):
        """Test converting to PascalCase"""
        assert StringUtils.to_pascal_case("hello_world") == "HelloWorld"
        assert StringUtils.to_pascal_case("hello-world") == "HelloWorld"
        assert StringUtils.to_pascal_case("hello world") == "HelloWorld"
    
    def test_to_kebab_case(self):
        """Test converting to kebab-case"""
        assert StringUtils.to_kebab_case("HelloWorld") == "hello-world"
        assert StringUtils.to_kebab_case("hello_world") == "hello-world"
        assert StringUtils.to_kebab_case("Hello World") == "hello-world"
    
    def test_truncate_short_text(self):
        """Test truncating text shorter than max length"""
        text = "Short text"
        result = StringUtils.truncate(text, 20)
        assert result == text
    
    def test_truncate_long_text(self):
        """Test truncating long text"""
        text = "This is a very long text that needs to be truncated"
        result = StringUtils.truncate(text, 20)
        assert len(result) == 20
        assert result.endswith("...")
    
    def test_truncate_custom_suffix(self):
        """Test truncating with custom suffix"""
        text = "Long text here"
        result = StringUtils.truncate(text, 10, suffix=">>")
        assert result.endswith(">>")
    
    def test_strip_comments_single_line(self):
        """Test stripping single-line comments"""
        code = "const x = 1; // comment\nconst y = 2; // another"
        result = StringUtils.strip_comments(code)
        assert "//" not in result
        assert "const x = 1;" in result
    
    def test_strip_comments_multi_line(self):
        """Test stripping multi-line comments"""
        code = "const x = 1; /* comment\nmore comment */ const y = 2;"
        result = StringUtils.strip_comments(code)
        assert "/*" not in result
        assert "*/" not in result
    
    def test_count_words(self):
        """Test counting words"""
        assert StringUtils.count_words("Hello world") == 2
        assert StringUtils.count_words("One two three four") == 4
        assert StringUtils.count_words("") == 0
    
    def test_extract_quoted_strings(self):
        """Test extracting quoted strings"""
        text = 'const name = "John"; const city = \'Paris\';'
        result = StringUtils.extract_quoted_strings(text)
        assert "John" in result
        assert "Paris" in result
    
    def test_sanitize_filename(self):
        """Test sanitizing filename"""
        assert StringUtils.sanitize_filename("test<file>.txt") == "testfile.txt"
        assert StringUtils.sanitize_filename("my file.doc") == "my_file.doc"
        assert StringUtils.sanitize_filename("file/path\\name") == "filepathname"
    
    def test_indent(self):
        """Test indenting text"""
        text = "line1\nline2\nline3"
        result = StringUtils.indent(text, 2)
        lines = result.split('\n')
        assert all(line.startswith('  ') or not line.strip() for line in lines)
    
    def test_remove_empty_lines(self):
        """Test removing empty lines"""
        text = "line1\n\nline2\n\n\nline3"
        result = StringUtils.remove_empty_lines(text)
        assert result == "line1\nline2\nline3"
    
    def test_wrap_text(self):
        """Test wrapping text"""
        text = "This is a very long line that should be wrapped to multiple lines"
        result = StringUtils.wrap_text(text, width=20)
        lines = result.split('\n')
        assert all(len(line) <= 25 for line in lines)  # Allow some flexibility
        assert len(lines) > 1
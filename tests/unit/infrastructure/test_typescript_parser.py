# =============================================================================
# tests/unit/infrastructure/test_typescript_parser.py
# =============================================================================
"""Unit tests for TypeScriptParser"""

import pytest
from src.infrastructure.parsers.typescript_parser import TypeScriptParser
from src.infrastructure.parsers.base_parser import ParseResult


class TestTypeScriptParser:
    """Test TypeScriptParser"""
    
    @pytest.fixture
    def parser(self):
        return TypeScriptParser()
    
    @pytest.fixture
    def simple_test_content(self):
        return """
import { Test } from '@nestjs/testing';
import { UserService } from './user.service';

const mockUser = {
  id: 1,
  name: 'Test User'
};

describe('UserService', () => {
  let service: UserService;
  
  beforeEach(() => {
    service = new UserService();
  });
  
  describe('findOne', () => {
    it('should return a user', () => {
      const result = service.findOne(1);
      expect(result).toEqual(mockUser);
    });
  });
  
  describe('create', () => {
    it('should create a user', () => {
      const result = service.create(mockUser);
      expect(result).toBeDefined();
    });
  });
});
"""
    
    def test_can_parse_spec_file(self, parser):
        """Test can_parse for .spec.ts files"""
        assert parser.can_parse('test.spec.ts')
        assert parser.can_parse('test.spec.tsx')
        assert parser.can_parse('path/to/test.spec.ts')
    
    def test_can_parse_test_file(self, parser):
        """Test can_parse for .test.ts files"""
        assert parser.can_parse('test.test.ts')
        assert parser.can_parse('test.test.tsx')
    
    def test_cannot_parse_non_test_file(self, parser):
        """Test can_parse returns False for non-test files"""
        assert not parser.can_parse('service.ts')
        assert not parser.can_parse('component.tsx')
        assert not parser.can_parse('index.js')
    
    def test_parse_returns_parse_result(self, parser, simple_test_content):
        """Test parse returns ParseResult"""
        result = parser.parse(simple_test_content)
        
        assert isinstance(result, ParseResult)
        assert hasattr(result, 'imports')
        assert hasattr(result, 'mock_data')
        assert hasattr(result, 'categories')
        assert hasattr(result, 'test_cases')
    
    def test_parse_extracts_imports(self, parser, simple_test_content):
        """Test parsing extracts import statements"""
        result = parser.parse(simple_test_content)
        
        assert len(result.imports) == 2
        assert any('@nestjs/testing' in imp for imp in result.imports)
    
    def test_parse_extracts_mocks(self, parser, simple_test_content):
        """Test parsing extracts mock data"""
        result = parser.parse(simple_test_content)
        
        assert len(result.mock_data) >= 1
        assert any(mock['name'] == 'mockUser' for mock in result.mock_data)
    
    def test_parse_extracts_categories(self, parser, simple_test_content):
        """Test parsing extracts test categories"""
        result = parser.parse(simple_test_content)
        
        assert 'findOne' in result.categories or 'create' in result.categories
    
    def test_parse_extracts_test_cases(self, parser, simple_test_content):
        """Test parsing extracts test cases"""
        result = parser.parse(simple_test_content)
        
        assert len(result.test_cases) >= 2
    
    def test_parse_extracts_setup_hooks(self, parser, simple_test_content):
        """Test parsing extracts setup hooks"""
        result = parser.parse(simple_test_content)
        
        assert 'beforeEach' in result.setup_hooks
    
    def test_parse_calculates_complexity(self, parser, simple_test_content):
        """Test parsing calculates complexity metrics"""
        result = parser.parse(simple_test_content)
        
        assert 'cyclomatic_complexity' in result.complexity_metrics
        assert result.complexity_metrics['cyclomatic_complexity'] > 0
    
    def test_parse_empty_file(self, parser):
        """Test parsing empty file"""
        result = parser.parse("")
        
        assert len(result.imports) == 0
        assert len(result.mock_data) == 0
        assert len(result.categories) == 0
        assert len(result.test_cases) == 0
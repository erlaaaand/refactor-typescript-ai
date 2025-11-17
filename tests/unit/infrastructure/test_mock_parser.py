# =============================================================================
# tests/unit/infrastructure/test_mock_parser.py
# =============================================================================
"""Unit tests for MockParser"""

import pytest
from src.infrastructure.parsers.mock_parser import MockParser, MockVariable


class TestMockParser:
    """Test MockParser"""
    
    @pytest.fixture
    def parser(self):
        return MockParser()
    
    @pytest.fixture
    def sample_code_lines(self):
        return [
            "import { Test } from '@nestjs/testing';",
            "",
            "const mockUser = {",
            "  id: 1,",
            "  name: 'Test User',",
            "  email: 'test@example.com'",
            "};",
            "",
            "const mockRepository = {",
            "  findOne: jest.fn(),",
            "  save: jest.fn()",
            "};",
            "",
            "const testData = [1, 2, 3];",
            "",
            "describe('Tests', () => {",
            "  // tests here",
            "});"
        ]
    
    def test_parse_mocks_returns_list(self, parser, sample_code_lines):
        """Test parse_mocks returns list of MockVariable"""
        mocks = parser.parse_mocks(sample_code_lines)
        
        assert isinstance(mocks, list)
        assert all(isinstance(mock, MockVariable) for mock in mocks)
    
    def test_parse_mocks_finds_mock_variables(self, parser, sample_code_lines):
        """Test parse_mocks finds mock variables"""
        mocks = parser.parse_mocks(sample_code_lines)
        
        mock_names = [mock.name for mock in mocks]
        assert 'mockUser' in mock_names
        assert 'mockRepository' in mock_names
    
    def test_parse_mocks_finds_test_data(self, parser, sample_code_lines):
        """Test parse_mocks finds test data variables"""
        mocks = parser.parse_mocks(sample_code_lines)
        
        mock_names = [mock.name for mock in mocks]
        assert 'testData' in mock_names
    
    def test_mock_variable_has_content(self, parser, sample_code_lines):
        """Test MockVariable contains content"""
        mocks = parser.parse_mocks(sample_code_lines)
        
        mock_user = next((m for m in mocks if m.name == 'mockUser'), None)
        assert mock_user is not None
        assert 'id: 1' in mock_user.content
        assert 'name:' in mock_user.content
    
    def test_infer_mock_type_object(self, parser):
        """Test inferring object mock type"""
        content = "const mockUser = { id: 1, name: 'Test' };"
        mock_type = parser._infer_mock_type(content)
        
        assert mock_type == 'object'
    
    def test_infer_mock_type_function(self, parser):
        """Test inferring function mock type"""
        content = "const mockFn = jest.fn();"
        mock_type = parser._infer_mock_type(content)
        
        assert mock_type == 'function'
    
    def test_infer_mock_type_repository(self, parser):
        """Test inferring repository mock type"""
        content = "const mockRepository = { findOne: jest.fn() };"
        mock_type = parser._infer_mock_type(content)
        
        assert mock_type == 'repository'
    
    def test_infer_mock_type_array(self, parser):
        """Test inferring array mock type"""
        content = "const testData = [1, 2, 3];"
        mock_type = parser._infer_mock_type(content)
        
        assert mock_type == 'array'
    
    def test_calculate_mock_complexity(self, parser):
        """Test calculating mock complexity"""
        simple_mock = "const mockUser = { id: 1 };"
        complex_mock = """
        const mockUser = {
          id: 1,
          name: 'Test',
          profile: {
            age: 30,
            address: {
              city: 'Test'
            }
          },
          getData: () => {}
        };
        """
        
        simple_complexity = parser._calculate_mock_complexity(simple_mock)
        complex_complexity = parser._calculate_mock_complexity(complex_mock)
        
        assert complex_complexity > simple_complexity
    
    def test_is_mock_variable_with_mock_prefix(self, parser):
        """Test identifying mock variables with 'mock' prefix"""
        assert parser._is_mock_variable('mockUser')
        assert parser._is_mock_variable('mockRepository')
        assert parser._is_mock_variable('mockData')
    
    def test_is_mock_variable_with_test_prefix(self, parser):
        """Test identifying mock variables with 'test' prefix"""
        assert parser._is_mock_variable('testData')
        assert parser._is_mock_variable('testUser')
    
    def test_is_not_mock_variable(self, parser):
        """Test not identifying regular variables as mocks"""
        assert not parser._is_mock_variable('service')
        assert not parser._is_mock_variable('controller')
        assert not parser._is_mock_variable('result')
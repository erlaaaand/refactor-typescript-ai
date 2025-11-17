# =============================================================================
# tests/unit/infrastructure/test_import_parser.py
# =============================================================================
"""Unit tests for ImportParser"""

import pytest
from src.infrastructure.parsers.import_parser import ImportParser, ImportStatement


class TestImportParser:
    """Test ImportParser"""
    
    @pytest.fixture
    def parser(self):
        return ImportParser()
    
    @pytest.fixture
    def sample_code(self):
        return """import { Test } from '@nestjs/testing';
import { UserEntity } from './entities/user.entity';
import type { ConfigService } from '@nestjs/config';
import * as request from 'supertest';
"""
    
    def test_parse_imports(self, parser, sample_code):
        """Test parsing import statements"""
        imports = parser.parse_imports(sample_code)
        
        assert len(imports) == 4
        assert all(isinstance(imp, ImportStatement) for imp in imports)
    
    def test_extract_imported_names(self, parser):
        """Test extracting imported names"""
        import_stmt = ImportStatement(
            raw="import { Test, Module } from '@nestjs/testing';",
            imports="{ Test, Module }",
            source="@nestjs/testing",
            is_type_import=False,
            line_number=0
        )
        
        names = parser.extract_imported_names(import_stmt)
        
        assert len(names) == 2
        assert 'Test' in names
        assert 'Module' in names
    
    def test_categorize_imports(self, parser, sample_code):
        """Test categorizing imports"""
        imports = parser.parse_imports(sample_code)
        categorized = parser.categorize_imports(imports)
        
        assert 'internal' in categorized
        assert 'external' in categorized
        assert 'types' in categorized
        
        # Check that internal import is detected
        assert len(categorized['internal']) == 1
        # Check that type import is detected
        assert len(categorized['types']) == 1
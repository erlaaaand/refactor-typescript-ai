# =============================================================================
# tests/unit/infrastructure/test_file_scanner.py
# =============================================================================
"""Unit tests for FileScanner"""

import pytest
from pathlib import Path
import tempfile
import shutil

from src.infrastructure.scanners.file_scanner import FileScanner


class TestFileScanner:
    """Test FileScanner"""
    
    @pytest.fixture
    def scanner(self):
        return FileScanner(max_workers=2)
    
    @pytest.fixture
    def temp_dir_with_files(self):
        """Create temporary directory with test files"""
        temp = Path(tempfile.mkdtemp())
        
        # Create test directory structure
        test_dir = temp / "src" / "users"
        test_dir.mkdir(parents=True)
        
        # Create test files
        (test_dir / "user.service.spec.ts").write_text("// test file")
        (test_dir / "user.controller.spec.ts").write_text("// test file")
        (test_dir / "user.entity.ts").write_text("// not a test file")
        
        # Create nested test directory
        nested = test_dir / "__tests__"
        nested.mkdir()
        (nested / "user.test.ts").write_text("// test file")
        
        # Create excluded directory
        node_modules = temp / "node_modules"
        node_modules.mkdir()
        (node_modules / "lib.spec.ts").write_text("// should be excluded")
        
        yield temp
        
        # Cleanup
        shutil.rmtree(temp)
    
    def test_scan_finds_test_files(self, scanner, temp_dir_with_files):
        """Test scan finds test files"""
        files = scanner.scan(temp_dir_with_files)
        
        assert len(files) > 0
        assert all(f.is_file() for f in files)
    
    def test_scan_finds_spec_files(self, scanner, temp_dir_with_files):
        """Test scan finds .spec.ts files"""
        files = scanner.scan(temp_dir_with_files)
        
        spec_files = [f for f in files if '.spec.' in f.name]
        assert len(spec_files) >= 2
    
    def test_scan_finds_test_files_pattern(self, scanner, temp_dir_with_files):
        """Test scan finds .test.ts files"""
        files = scanner.scan(temp_dir_with_files)
        
        test_files = [f for f in files if '.test.' in f.name]
        assert len(test_files) >= 1
    
    def test_scan_excludes_node_modules(self, scanner, temp_dir_with_files):
        """Test scan excludes node_modules directory"""
        files = scanner.scan(temp_dir_with_files)
        
        node_modules_files = [f for f in files if 'node_modules' in f.parts]
        assert len(node_modules_files) == 0
    
    def test_scan_excludes_non_test_files(self, scanner, temp_dir_with_files):
        """Test scan excludes non-test files"""
        files = scanner.scan(temp_dir_with_files)
        
        entity_files = [f for f in files if 'entity.ts' in f.name]
        assert len(entity_files) == 0
    
    def test_should_include_test_file(self, scanner):
        """Test _should_include for test files"""
        test_file = Path("src/user.spec.ts")
        assert scanner._should_include(test_file)
        
        test_file2 = Path("src/user.test.tsx")
        assert scanner._should_include(test_file2)
    
    def test_should_not_include_regular_file(self, scanner):
        """Test _should_include excludes regular files"""
        regular_file = Path("src/user.service.ts")
        assert not scanner._should_include(regular_file)
    
    def test_should_not_include_excluded_dir(self, scanner):
        """Test _should_include excludes files in excluded directories"""
        excluded_file = Path("node_modules/lib/test.spec.ts")
        assert not scanner._should_include(excluded_file)
    
    def test_scan_empty_directory(self, scanner):
        """Test scanning empty directory"""
        temp = Path(tempfile.mkdtemp())
        
        try:
            files = scanner.scan(temp)
            assert len(files) == 0
        finally:
            shutil.rmtree(temp)
    
    def test_custom_exclude_dirs(self):
        """Test scanner with custom exclude directories"""
        scanner = FileScanner(max_workers=1)
        scanner.exclude_dirs = {'node_modules', 'dist', 'custom_exclude'}
        
        excluded_file = Path("custom_exclude/test.spec.ts")
        assert not scanner._should_include(excluded_file)
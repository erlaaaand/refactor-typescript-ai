# =============================================================================
# tests/unit/shared/test_file_utils.py
# =============================================================================
"""Unit tests for FileUtils"""

import pytest
from pathlib import Path
import tempfile
import shutil

from src.shared.utils.file_utils import FileUtils


class TestFileUtils:
    """Test FileUtils"""
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory"""
        temp = Path(tempfile.mkdtemp())
        yield temp
        shutil.rmtree(temp)
    
    def test_ensure_directory_creates_dir(self, temp_dir):
        """Test ensure_directory creates directory"""
        new_dir = temp_dir / "new" / "nested" / "dir"
        result = FileUtils.ensure_directory(new_dir)
        
        assert result.exists()
        assert result.is_dir()
    
    def test_ensure_directory_existing_dir(self, temp_dir):
        """Test ensure_directory with existing directory"""
        result = FileUtils.ensure_directory(temp_dir)
        assert result == temp_dir
        assert result.exists()
    
    def test_backup_file(self, temp_dir):
        """Test backing up file"""
        # Create test file
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")
        
        # Backup file
        backup_path = FileUtils.backup_file(test_file)
        
        assert backup_path.exists()
        assert backup_path.read_text() == "test content"
        assert backup_path.parent.name == "backups"
    
    def test_backup_file_not_found(self, temp_dir):
        """Test backing up non-existent file raises error"""
        non_existent = temp_dir / "notfound.txt"
        
        with pytest.raises(FileNotFoundError):
            FileUtils.backup_file(non_existent)
    
    def test_safe_write_new_file(self, temp_dir):
        """Test safely writing new file"""
        new_file = temp_dir / "new.txt"
        content = "test content"
        
        success = FileUtils.safe_write(new_file, content, backup=False)
        
        assert success
        assert new_file.exists()
        assert new_file.read_text() == content
    
    def test_safe_write_existing_file_with_backup(self, temp_dir):
        """Test safely writing existing file with backup"""
        existing_file = temp_dir / "existing.txt"
        existing_file.write_text("original")
        
        success = FileUtils.safe_write(existing_file, "new content", backup=True)
        
        assert success
        assert existing_file.read_text() == "new content"
        
        # Check backup was created
        backup_dir = temp_dir / "backups"
        assert backup_dir.exists()
    
    def test_read_file(self, temp_dir):
        """Test reading file"""
        test_file = temp_dir / "test.txt"
        content = "test content"
        test_file.write_text(content)
        
        result = FileUtils.read_file(test_file)
        assert result == content
    
    def test_read_file_not_found(self, temp_dir):
        """Test reading non-existent file raises error"""
        non_existent = temp_dir / "notfound.txt"
        
        with pytest.raises(FileNotFoundError):
            FileUtils.read_file(non_existent)
    
    def test_get_relative_path(self, temp_dir):
        """Test getting relative path"""
        root = temp_dir
        file_path = temp_dir / "src" / "test.ts"
        
        relative = FileUtils.get_relative_path(file_path, root)
        assert relative == Path("src/test.ts")
    
    def test_find_files(self, temp_dir):
        """Test finding files"""
        # Create test files
        (temp_dir / "test1.spec.ts").write_text("test")
        (temp_dir / "test2.spec.ts").write_text("test")
        (temp_dir / "service.ts").write_text("service")
        
        # Create excluded directory
        node_modules = temp_dir / "node_modules"
        node_modules.mkdir()
        (node_modules / "test.spec.ts").write_text("test")
        
        files = FileUtils.find_files(temp_dir, ["*.spec.ts"])
        
        assert len(files) == 2
        assert all("spec.ts" in f.name for f in files)
        assert not any("node_modules" in f.parts for f in files)
    
    def test_get_file_stats(self, temp_dir):
        """Test getting file statistics"""
        test_file = temp_dir / "test.txt"
        content = "line1\nline2\nline3\n\nline4"
        test_file.write_text(content)
        
        stats = FileUtils.get_file_stats(test_file)
        
        assert 'size_bytes' in stats
        assert 'total_lines' in stats
        assert 'non_empty_lines' in stats
        assert 'last_modified' in stats
        assert stats['total_lines'] == 5
        assert stats['non_empty_lines'] == 4
    
    def test_clean_directory(self, temp_dir):
        """Test cleaning directory"""
        # Create files
        (temp_dir / "keep.txt").write_text("keep")
        (temp_dir / "remove.txt").write_text("remove")
        (temp_dir / "keep.log").write_text("keep")
        
        FileUtils.clean_directory(temp_dir, keep_patterns=["*.txt"])
        
        # Only .txt files should remain
        remaining = list(temp_dir.glob("*"))
        assert len(remaining) == 2
        assert all(f.suffix == ".txt" for f in remaining)
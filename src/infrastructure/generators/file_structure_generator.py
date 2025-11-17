# =============================================================================
# src/infrastructure/generators/file_structure_generator.py
# =============================================================================
"""File Structure Generator - Generates directory and file structures"""

from pathlib import Path
from typing import List, Dict
from dataclasses import dataclass


@dataclass
class FileStructure:
    """Represents a file structure to be generated"""
    base_path: Path
    files: List[Path]
    directories: List[Path]
    description: str


class FileStructureGenerator:
    """Generates file and directory structures for refactored code"""
    
    def __init__(self, base_output_dir: Path):
        self.base_output_dir = base_output_dir
    
    def generate_split_structure(self, original_file: Path, 
                                 split_count: int,
                                 strategy: str = 'category') -> FileStructure:
        """
        Generate file structure for split refactoring
        
        Args:
            original_file: Original test file path
            split_count: Number of files to split into
            strategy: Split strategy ('category', 'concern', 'feature')
        """
        base_name = original_file.stem.replace('.spec', '').replace('.test', '')
        parent_dir = original_file.parent
        
        files = []
        for i in range(split_count):
            if strategy == 'category':
                suffix = f'.category{i+1}.spec.ts'
            elif strategy == 'concern':
                suffix = f'.part{i+1}.spec.ts'
            else:
                suffix = f'.split{i+1}.spec.ts'
            
            new_file = parent_dir / f"{base_name}{suffix}"
            files.append(new_file)
        
        return FileStructure(
            base_path=parent_dir,
            files=files,
            directories=[parent_dir],
            description=f'Split {original_file.name} into {split_count} files by {strategy}'
        )
    
    def generate_extract_shared_structure(self, original_file: Path) -> FileStructure:
        """Generate structure for extracting shared utilities"""
        parent_dir = original_file.parent
        
        utils_file = parent_dir / 'test-utils.ts'
        fixtures_file = parent_dir / 'test-fixtures.ts'
        mocks_file = parent_dir / 'test-mocks.ts'
        
        return FileStructure(
            base_path=parent_dir,
            files=[utils_file, fixtures_file, mocks_file],
            directories=[parent_dir],
            description=f'Extract shared utilities from {original_file.name}'
        )
    
    def generate_modular_structure(self, original_file: Path,
                                   modules: List[str]) -> FileStructure:
        """Generate modular test structure"""
        base_name = original_file.stem.replace('.spec', '').replace('.test', '')
        parent_dir = original_file.parent
        
        # Create subdirectory for module
        module_dir = parent_dir / f"{base_name}.tests"
        
        files = []
        for module in modules:
            module_safe = module.lower().replace(' ', '-')
            test_file = module_dir / f"{module_safe}.spec.ts"
            files.append(test_file)
        
        # Add index and shared files
        files.append(module_dir / 'index.ts')
        files.append(module_dir / 'shared.ts')
        
        return FileStructure(
            base_path=module_dir,
            files=files,
            directories=[module_dir],
            description=f'Create modular structure for {original_file.name}'
        )
    
    def create_structure(self, structure: FileStructure, 
                        dry_run: bool = False) -> bool:
        """
        Create the file structure on disk
        
        Args:
            structure: FileStructure to create
            dry_run: If True, only simulate creation
        """
        if dry_run:
            print(f"[DRY RUN] Would create structure:")
            print(f"  Base: {structure.base_path}")
            print(f"  Directories: {len(structure.directories)}")
            print(f"  Files: {len(structure.files)}")
            return True
        
        try:
            # Create directories
            for directory in structure.directories:
                directory.mkdir(parents=True, exist_ok=True)
            
            # Create empty files (content to be filled later)
            for file_path in structure.files:
                if not file_path.exists():
                    file_path.touch()
            
            return True
        except Exception as e:
            print(f"Error creating structure: {e}")
            return False
    
    def generate_migration_map(self, original_file: Path,
                               new_structure: FileStructure) -> Dict[str, str]:
        """Generate mapping from old to new file structure"""
        return {
            'original': str(original_file),
            'strategy': new_structure.description,
            'base_path': str(new_structure.base_path),
            'new_files': [str(f) for f in new_structure.files],
            'created_dirs': [str(d) for d in new_structure.directories]
        }
    
    def cleanup_structure(self, structure: FileStructure) -> bool:
        """Remove created structure (for rollback)"""
        try:
            for file_path in structure.files:
                if file_path.exists():
                    file_path.unlink()
            
            for directory in reversed(structure.directories):
                if directory.exists() and not any(directory.iterdir()):
                    directory.rmdir()
            
            return True
        except Exception:
            return False
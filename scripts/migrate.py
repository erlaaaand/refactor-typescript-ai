# =============================================================================
# scripts/migrate.py
# =============================================================================
"""Migration script to refactor existing codebase"""

import shutil
from pathlib import Path
from typing import Dict, List
import re


class CodeMigrator:
    """Migrates code from old structure to new structure"""
    
    def __init__(self, source_root: Path, target_root: Path):
        self.source_root = source_root
        self.target_root = target_root
        
        # Migration mapping
        self.migration_map = {
            # Old -> New
            'models/test_file.py': [
                'src/domain/entities/test_file.py',
                'src/domain/value_objects/file_metadata.py'
            ],
            'models/pattern.py': [
                'src/domain/entities/pattern.py'
            ],
            'models/refactor_plan.py': [
                'src/domain/entities/refactor_plan.py'
            ],
            'core/code_parser.py': [
                'src/infrastructure/parsers/base_parser.py',
                'src/infrastructure/parsers/typescript_parser.py',
                'src/infrastructure/parsers/import_parser.py',
                'src/infrastructure/parsers/mock_parser.py',
                'src/infrastructure/parsers/test_structure_parser.py'
            ],
            'core/pattern_analyzer.py': [
                'src/infrastructure/analyzers/base_analyzer.py',
                'src/infrastructure/analyzers/complexity_analyzer.py',
                'src/infrastructure/analyzers/quality_analyzer.py',
                'src/infrastructure/analyzers/smell_detector.py'
            ],
            'core/file_scanner.py': [
                'src/infrastructure/scanners/file_scanner.py',
                'src/infrastructure/scanners/parallel_scanner.py'
            ],
            'core/refactor_engine.py': [
                'src/infrastructure/generators/code_generator.py',
                'src/infrastructure/generators/import_optimizer.py',
                'src/infrastructure/generators/file_structure_generator.py'
            ],
            'training/phase1_learning.py': [
                'src/application/use_cases/analyze_test_files.py',
                'src/application/services/analysis_service.py'
            ],
            'training/phase2_practice.py': [
                'src/application/use_cases/generate_refactor_plan.py',
                'src/application/services/planning_service.py'
            ],
            'training/phase3_execution.py': [
                'src/application/use_cases/execute_refactoring.py',
                'src/application/services/execution_service.py'
            ],
            'main.py': [
                'src/interfaces/cli/main.py',
                'src/interfaces/cli/commands/analyze_command.py',
                'src/interfaces/cli/commands/learn_command.py'
            ]
        }
    
    def migrate(self):
        """Execute migration"""
        print("\n🚀 Starting migration...\n")
        
        # Step 1: Backup old code
        print("📦 Step 1: Creating backup...")
        self._create_backup()
        print("   ✓ Backup created\n")
        
        # Step 2: Create new structure
        print("🏗️  Step 2: Creating new structure...")
        self._create_structure()
        print("   ✓ Structure created\n")
        
        # Step 3: Extract and split code
        print("✂️  Step 3: Extracting and splitting code...")
        self._extract_code()
        print("   ✓ Code extracted\n")
        
        # Step 4: Update imports
        print("🔗 Step 4: Updating imports...")
        self._update_imports()
        print("   ✓ Imports updated\n")
        
        # Step 5: Generate stubs for missing files
        print("📝 Step 5: Generating stubs...")
        self._generate_stubs()
        print("   ✓ Stubs generated\n")
        
        print("✅ Migration complete!\n")
        print("Next steps:")
        print("  1. Review generated code")
        print("  2. Run: pytest tests/")
        print("  3. Run: mypy src/")
        print("  4. Fix any remaining issues")
    
    def _create_backup(self):
        """Create backup of current code"""
        import tarfile
        from datetime import datetime
        
        backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tar.gz"
        
        with tarfile.open(backup_name, "w:gz") as tar:
            for item in ['core', 'models', 'training', 'utils', 'main.py', 'config.yaml']:
                if Path(item).exists():
                    tar.add(item)
        
        print(f"   Backup saved: {backup_name}")
    
    def _create_structure(self):
        """Create new directory structure"""
        from scripts.setup_structure import create_directory_structure
        create_directory_structure()
    
    def _extract_code(self):
        """Extract code from old files to new files"""
        for old_file, new_files in self.migration_map.items():
            old_path = self.source_root / old_file
            
            if not old_path.exists():
                continue
            
            print(f"   Processing {old_file}...")
            
            # For now, copy to first target
            # In real implementation, would intelligently split
            if new_files:
                new_path = self.target_root / new_files[0]
                new_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Copy file
                shutil.copy2(old_path, new_path)
                print(f"      → {new_files[0]}")
    
    def _update_imports(self):
        """Update import statements in all files"""
        import_mapping = {
            'from models.': 'from src.domain.entities.',
            'from core.': 'from src.infrastructure.',
            'from training.': 'from src.application.',
            'from utils.': 'from src.shared.utils.'
        }
        
        # Find all Python files in new structure
        for py_file in self.target_root.rglob('src/**/*.py'):
            if py_file.name == '__init__.py':
                continue
            
            content = py_file.read_text()
            original = content
            
            # Replace imports
            for old, new in import_mapping.items():
                content = content.replace(old, new)
            
            # Write back if changed
            if content != original:
                py_file.write_text(content)
                print(f"   Updated imports in {py_file.relative_to(self.target_root)}")
    
    def _generate_stubs(self):
        """Generate stub files for missing implementations"""
        stubs = {
            'src/shared/exceptions/base_exceptions.py': '''"""Base Exceptions"""

class DomainException(Exception):
    """Base domain exception"""
    pass

class ValidationException(DomainException):
    """Validation error"""
    pass

class ParsingException(DomainException):
    """Parsing error"""
    pass
''',
            'src/shared/validators/file_validator.py': '''"""File Validator"""

from pathlib import Path

class FileValidator:
    """Validates file operations"""
    
    @staticmethod
    def validate_path(path: Path) -> bool:
        """Validate file path"""
        return path.exists() and path.is_file()
    
    @staticmethod
    def validate_test_file(path: Path) -> bool:
        """Validate test file"""
        return path.suffix in ['.ts', '.tsx'] and 'spec' in path.name
'''
        }
        
        for file_path, content in stubs.items():
            full_path = self.target_root / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content)
            print(f"   Created {file_path}")


def main():
    """Main execution"""
    import sys
    
    source = Path('.')
    target = Path('.')
    
    if len(sys.argv) > 1:
        source = Path(sys.argv[1])
    if len(sys.argv) > 2:
        target = Path(sys.argv[2])
    
    migrator = CodeMigrator(source, target)
    migrator.migrate()


if __name__ == "__main__":
    main()
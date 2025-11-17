#!/usr/bin/env python3
"""
Setup New Directory Structure
Creates the complete refactored directory structure
"""

from pathlib import Path
from typing import List


def create_directory_structure():
    """Create complete directory structure for refactored codebase"""
    
    directories = [
        # Domain Layer
        "src/domain/entities",
        "src/domain/value_objects",
        "src/domain/repositories",
        
        # Application Layer
        "src/application/use_cases",
        "src/application/services",
        "src/application/dto",
        
        # Infrastructure Layer
        "src/infrastructure/parsers",
        "src/infrastructure/analyzers",
        "src/infrastructure/scanners",
        "src/infrastructure/generators",
        "src/infrastructure/persistence",
        
        # Interface Layer
        "src/interfaces/cli/commands",
        "src/interfaces/cli/presenters",
        "src/interfaces/config",
        
        # Shared Kernel
        "src/shared/exceptions",
        "src/shared/validators",
        "src/shared/utils",
        
        # Tests
        "tests/unit/domain",
        "tests/unit/application",
        "tests/unit/infrastructure",
        "tests/integration",
        "tests/e2e",
        "tests/fixtures",
        
        # Config
        "config",
        
        # Docs
        "docs/architecture",
        "docs/api",
        "docs/guides",
        
        # Scripts
        "scripts",
        
        # Output
        "output/training_data",
        "output/practice_runs",
        "output/execution_results",
        "output/backups",
    ]
    
    print("🏗️  Creating directory structure...")
    
    for directory in directories:
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        
        # Create __init__.py for Python packages
        if path.parts[0] in ['src', 'tests']:
            init_file = path / "__init__.py"
            if not init_file.exists():
                init_file.write_text('"""Package initialization."""\n')
        
        print(f"  ✓ {directory}")
    
    print("\n✅ Directory structure created!")
    print("\n📝 Next steps:")
    print("  1. Run: python scripts/migrate.py")
    print("  2. Update imports")
    print("  3. Run tests")


def create_config_files():
    """Create initial configuration files"""
    
    # pyproject.toml
    pyproject_content = '''[build-system]
requires = ["setuptools>=65.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "test-refactor-ai"
version = "2.1.0"
description = "Intelligent TypeScript test file refactoring with AI"
readme = "README.md"
requires-python = ">=3.8"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "your@email.com"}
]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
]

dependencies = [
    "pydantic>=2.0.0",
    "rich>=13.0.0",
    "typer>=0.9.0",
    "pyyaml>=6.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "pytest-asyncio>=0.21.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
    "mypy>=1.5.0",
    "pre-commit>=3.4.0",
]

[project.scripts]
refactor-ai = "src.interfaces.cli.main:app"

[tool.setuptools.packages.find]
where = ["src"]

[tool.black]
line-length = 100
target-version = ["py38", "py39", "py310", "py311"]

[tool.ruff]
line-length = 100
select = ["E", "F", "I", "N", "W", "UP"]
ignore = []
target-version = "py38"

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
no_implicit_optional = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --cov=src --cov-report=html --cov-report=term"
'''
    
    Path("pyproject.toml").write_text(pyproject_content)
    print("  ✓ pyproject.toml")
    
    # .gitignore
    gitignore_content = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# Project specific
output/
.scan_cache.json
*.log
_old_*/

# OS
.DS_Store
Thumbs.db
'''
    
    Path(".gitignore").write_text(gitignore_content)
    print("  ✓ .gitignore")
    
    # Pre-commit config
    precommit_content = '''repos:
  - repo: https://github.com/psf/black
    rev: 23.9.1
    hooks:
      - id: black

  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.5.1
    hooks:
      - id: mypy
        additional_dependencies: [pydantic>=2.0.0]

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
'''
    
    Path(".pre-commit-config.yaml").write_text(precommit_content)
    print("  ✓ .pre-commit-config.yaml")


def main():
    """Main execution"""
    print("\n" + "="*70)
    print("🚀 Test Refactor AI - Structure Setup")
    print("="*70 + "\n")
    
    create_directory_structure()
    
    print("\n📦 Creating configuration files...")
    create_config_files()
    
    print("\n✅ Setup complete!")
    print("\n📚 Documentation:")
    print("  - Architecture: docs/architecture/")
    print("  - API Reference: docs/api/")
    print("  - Development Guide: docs/guides/")
    
    print("\n🔧 Install development tools:")
    print("  pip install -e \".[dev]\"")
    print("  pre-commit install")
    
    print("\n🧪 Run tests:")
    print("  pytest tests/ -v")
    
    print("\n🎨 Format code:")
    print("  black src/ tests/")
    print("  ruff src/ tests/ --fix")
    
    print("\n📊 Type checking:")
    print("  mypy src/")


if __name__ == "__main__":
    main()
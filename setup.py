# =============================================================================
# setup.py
# =============================================================================
"""Setup configuration for Test Refactor AI"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
def read_requirements(filename):
    """Read requirements from file"""
    req_file = Path(__file__).parent / filename
    if req_file.exists():
        return [
            line.strip() 
            for line in req_file.read_text().splitlines()
            if line.strip() and not line.startswith('#')
        ]
    return []

setup(
    name="test-refactor-ai",
    version="2.1.0",
    description="Intelligent TypeScript test file refactoring with AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your@email.com",
    url="https://github.com/yourusername/test-refactor-ai",
    
    # Package discovery
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    
    # Python version requirement
    python_requires=">=3.8",
    
    # Dependencies
    install_requires=[
        "pydantic>=2.0.0",
        "rich>=13.0.0",
        "typer>=0.9.0",
        "pyyaml>=6.0.0",
    ],
    
    # Optional dependencies
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "ruff>=0.1.0",
            "mypy>=1.5.0",
            "pre-commit>=3.4.0",
            "types-PyYAML>=6.0.0",
        ],
        "docs": [
            "sphinx>=7.0.0",
            "sphinx-rtd-theme>=1.3.0",
        ],
    },
    
    # Entry points
    entry_points={
        "console_scripts": [
            "refactor-ai=src.interfaces.cli.main:app",
        ],
    },
    
    # Package metadata
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
    ],
    
    keywords="typescript testing refactoring ai code-quality",
    
    # Include package data
    include_package_data=True,
    zip_safe=False,
)
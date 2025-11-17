# =============================================================================
# src/infrastructure/__init__.py
# =============================================================================
"""
Infrastructure Layer Package

This layer contains implementations of technical details and external concerns.
It provides concrete implementations of interfaces defined in the domain layer.

Components:
- Parsers: Code parsing implementations (TypeScript, imports, mocks, etc.)
- Analyzers: Code analysis implementations (complexity, quality, smells)
- Scanners: File system scanning implementations
- Generators: Code generation implementations
- Persistence: Data storage implementations (file-based, cache)
"""

from .parsers import (
    BaseParser,
    ParseResult,
    TypeScriptParser,
    ImportParser,
    ImportStatement,
    MockParser,
    MockVariable,
    TestStructureParser,
    TestBlock,
    BlockType
)

from .analyzers import (
    BaseAnalyzer,
    ComplexityAnalyzer,
    QualityAnalyzer,
    SmellDetector,
    CodeSmell
)

from .scanners import (
    FileScanner,
    ParallelScanner,
    ScanResult
)

from .generators import (
    CodeGenerator,
    ImportOptimizer,
    OptimizedImports,
    FileStructureGenerator,
    FileStructure
)

from .persistence import (
    FileTestFileRepository,
    CacheStorage,
    CacheEntry,
    JSONSerializer
)

__all__ = [
    # Parsers
    'BaseParser',
    'ParseResult',
    'TypeScriptParser',
    'ImportParser',
    'ImportStatement',
    'MockParser',
    'MockVariable',
    'TestStructureParser',
    'TestBlock',
    'BlockType',
    # Analyzers
    'BaseAnalyzer',
    'ComplexityAnalyzer',
    'QualityAnalyzer',
    'SmellDetector',
    'CodeSmell',
    # Scanners
    'FileScanner',
    'ParallelScanner',
    'ScanResult',
    # Generators
    'CodeGenerator',
    'ImportOptimizer',
    'OptimizedImports',
    'FileStructureGenerator',
    'FileStructure',
    # Persistence
    'FileTestFileRepository',
    'CacheStorage',
    'CacheEntry',
    'JSONSerializer'
]

__version__ = '2.1.0'
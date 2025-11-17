# =============================================================================
# src/infrastructure/parsers/import_parser.py
# =============================================================================
"""Import Statement Parser"""

import re
from typing import List, Dict
from dataclasses import dataclass


@dataclass
class ImportStatement:
    """Represents a parsed import statement"""
    raw: str
    imports: str
    source: str
    is_type_import: bool
    line_number: int


class ImportParser:
    """Parser for TypeScript import statements"""
    
    IMPORT_PATTERN = re.compile(
        r'^import\s+(.+?)\s+from\s+[\'"](.+?)[\'"]',
        re.MULTILINE
    )
    
    def parse_imports(self, content: str) -> List[ImportStatement]:
        """Extract all import statements"""
        imports = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            match = self.IMPORT_PATTERN.match(line.strip())
            if match:
                imports.append(ImportStatement(
                    raw=line.strip(),
                    imports=match.group(1),
                    source=match.group(2),
                    is_type_import='type' in match.group(1),
                    line_number=i
                ))
        
        return imports
    
    def extract_imported_names(self, import_stmt: ImportStatement) -> List[str]:
        """Extract individual imported names"""
        imports_str = import_stmt.imports
        
        # Handle default import
        if not '{' in imports_str:
            return [imports_str.strip()]
        
        # Handle named imports
        match = re.search(r'\{(.+?)\}', imports_str)
        if match:
            names = match.group(1).split(',')
            return [name.strip().split(' as ')[0].strip() for name in names]
        
        return []
    
    def categorize_imports(self, imports: List[ImportStatement]) -> Dict[str, List[ImportStatement]]:
        """Categorize imports by type"""
        categorized = {
            'internal': [],
            'external': [],
            'test_utils': [],
            'types': []
        }
        
        for imp in imports:
            if imp.is_type_import:
                categorized['types'].append(imp)
            elif imp.source.startswith('.'):
                categorized['internal'].append(imp)
            elif 'test' in imp.source or 'mock' in imp.source:
                categorized['test_utils'].append(imp)
            else:
                categorized['external'].append(imp)
        
        return categorized
# =============================================================================
# src/infrastructure/generators/import_optimizer.py
# =============================================================================
"""Import Optimizer - Optimizes and organizes import statements"""

from typing import List, Dict, Set
from dataclasses import dataclass


@dataclass
class OptimizedImports:
    """Optimized import structure"""
    external: List[str]
    internal: List[str]
    types: List[str]
    test_utils: List[str]


class ImportOptimizer:
    """Optimizes import statements in test files"""
    
    def __init__(self):
        self.external_packages = {
            '@nestjs', '@angular', 'react', 'vue', 'lodash',
            'axios', 'rxjs', 'moment', 'date-fns'
        }
    
    def optimize(self, imports: List[str]) -> OptimizedImports:
        """Optimize and categorize imports"""
        
        external = []
        internal = []
        types = []
        test_utils = []
        
        for imp in imports:
            if 'type' in imp.lower():
                types.append(imp)
            elif any(pkg in imp for pkg in ['test', 'mock', 'stub']):
                test_utils.append(imp)
            elif self._is_external(imp):
                external.append(imp)
            else:
                internal.append(imp)
        
        return OptimizedImports(
            external=self._sort_imports(external),
            internal=self._sort_imports(internal),
            types=self._sort_imports(types),
            test_utils=self._sort_imports(test_utils)
        )
    
    def _is_external(self, import_statement: str) -> bool:
        """Check if import is external package"""
        return any(pkg in import_statement for pkg in self.external_packages)
    
    def _sort_imports(self, imports: List[str]) -> List[str]:
        """Sort imports alphabetically"""
        return sorted(imports, key=lambda x: x.lower())
    
    def remove_unused(self, imports: List[str], content: str) -> List[str]:
        """Remove unused imports"""
        used_imports = []
        
        for imp in imports:
            # Extract imported names
            names = self._extract_names(imp)
            
            # Check if used in content
            if any(name in content for name in names):
                used_imports.append(imp)
        
        return used_imports
    
    def _extract_names(self, import_statement: str) -> List[str]:
        """Extract imported names from statement"""
        import re
        
        # Match { name1, name2 } pattern
        match = re.search(r'\{([^}]+)\}', import_statement)
        if match:
            names_str = match.group(1)
            return [n.strip().split(' as ')[0] for n in names_str.split(',')]
        
        # Match default import
        match = re.match(r'import\s+(\w+)', import_statement)
        if match:
            return [match.group(1)]
        
        return []
    
    def merge_imports(self, imports: List[str]) -> List[str]:
        """Merge imports from same source"""
        source_map: Dict[str, Set[str]] = {}
        
        for imp in imports:
            source = self._extract_source(imp)
            names = self._extract_names(imp)
            
            if source not in source_map:
                source_map[source] = set()
            
            source_map[source].update(names)
        
        # Reconstruct imports
        merged = []
        for source, names in source_map.items():
            if len(names) == 1:
                merged.append(f"import {list(names)[0]} from '{source}';")
            else:
                names_str = ', '.join(sorted(names))
                merged.append(f"import {{ {names_str} }} from '{source}';")
        
        return merged
    
    def _extract_source(self, import_statement: str) -> str:
        """Extract source from import statement"""
        import re
        
        match = re.search(r"from\s+['\"]([^'\"]+)['\"]", import_statement)
        if match:
            return match.group(1)
        
        return ""
    
    def generate_import_block(self, optimized: OptimizedImports) -> str:
        """Generate formatted import block"""
        blocks = []
        
        if optimized.external:
            blocks.append('\n'.join(optimized.external))
        
        if optimized.types:
            blocks.append('\n'.join(optimized.types))
        
        if optimized.internal:
            blocks.append('\n'.join(optimized.internal))
        
        if optimized.test_utils:
            blocks.append('\n'.join(optimized.test_utils))
        
        return '\n\n'.join(blocks)
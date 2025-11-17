# =============================================================================
# src/infrastructure/persistence/pattern_storage.py
# =============================================================================
"""Pattern Repository Implementation"""

import json
from pathlib import Path
from typing import List, Optional

from ...domain.entities.pattern import Pattern, PatternType, PatternFrequency
from ...domain.repositories.pattern_repository import PatternRepository


class FilePatternRepository(PatternRepository):
    """File-based implementation of PatternRepository"""
    
    def __init__(self, storage_dir: Path):
        self.storage_dir = storage_dir
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self._cache: dict[str, Pattern] = {}
    
    def find_by_id(self, pattern_id: str) -> Optional[Pattern]:
        """Find pattern by ID"""
        if pattern_id in self._cache:
            return self._cache[pattern_id]
        
        pattern_file = self.storage_dir / f"pattern_{pattern_id}.json"
        if pattern_file.exists():
            data = json.loads(pattern_file.read_text())
            return self._dict_to_pattern(data)
        
        return None
    
    def find_all(self) -> List[Pattern]:
        """Find all patterns"""
        patterns = []
        
        all_patterns_file = self.storage_dir / "all_patterns.json"
        if all_patterns_file.exists():
            data = json.loads(all_patterns_file.read_text())
            patterns = [self._dict_to_pattern(p) for p in data]
        
        return patterns
    
    def find_by_type(self, pattern_type: PatternType) -> List[Pattern]:
        """Find patterns by type"""
        all_patterns = self.find_all()
        return [p for p in all_patterns if p.type == pattern_type]
    
    def find_by_frequency(self, frequency: PatternFrequency) -> List[Pattern]:
        """Find patterns by frequency"""
        all_patterns = self.find_all()
        return [p for p in all_patterns if p.frequency == frequency]
    
    def find_significant(self) -> List[Pattern]:
        """Find significant patterns"""
        all_patterns = self.find_all()
        return [p for p in all_patterns if p.is_significant()]
    
    def find_good_practices(self) -> List[Pattern]:
        """Find patterns marked as good practices"""
        all_patterns = self.find_all()
        return [p for p in all_patterns if p.is_good_practice]
    
    def save(self, pattern: Pattern) -> None:
        """Save pattern"""
        self._cache[pattern.id] = pattern
        
        # Save individual pattern
        pattern_file = self.storage_dir / f"pattern_{pattern.id}.json"
        pattern_file.write_text(json.dumps(pattern.to_dict(), indent=2))
    
    def save_all(self, patterns: List[Pattern]) -> None:
        """Save multiple patterns"""
        for pattern in patterns:
            self.save(pattern)
        
        # Save all patterns list
        all_data = [p.to_dict() for p in patterns]
        all_file = self.storage_dir / "all_patterns.json"
        all_file.write_text(json.dumps(all_data, indent=2))
    
    def delete(self, pattern_id: str) -> bool:
        """Delete pattern by ID"""
        if pattern_id in self._cache:
            del self._cache[pattern_id]
        
        pattern_file = self.storage_dir / f"pattern_{pattern_id}.json"
        if pattern_file.exists():
            pattern_file.unlink()
            return True
        
        return False
    
    def update_occurrence(self, pattern_id: str, example: str) -> None:
        """Update pattern occurrence count"""
        pattern = self.find_by_id(pattern_id)
        if pattern:
            pattern.add_occurrence(example)
            self.save(pattern)
    
    def _dict_to_pattern(self, data: dict) -> Pattern:
        """Convert dictionary to Pattern entity"""
        from datetime import datetime
        
        return Pattern(
            id=data['id'],
            type=PatternType(data['type']),
            name=data['name'],
            description=data['description'],
            examples=data.get('examples', []),
            occurrences=data.get('occurrences', 0),
            total_files=data.get('total_files', 0),
            frequency=PatternFrequency(data['frequency']) if data.get('frequency') else None,
            confidence=data.get('confidence', 0.0),
            discovered_at=datetime.fromisoformat(data['discovered_at']),
            last_seen=datetime.fromisoformat(data['last_seen']),
            related_patterns=data.get('related_patterns', []),
            is_good_practice=data.get('is_good_practice', True),
            recommendation=data.get('recommendation')
        )
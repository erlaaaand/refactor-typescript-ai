# =============================================================================
# src/infrastructure/persistence/cache_storage.py
# =============================================================================
"""Cache Storage - In-memory and file-based caching"""

import json
import pickle
from pathlib import Path
from typing import Any, Optional, Dict
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict


@dataclass
class CacheEntry:
    """Represents a cached item"""
    key: str
    value: Any
    created_at: datetime
    expires_at: Optional[datetime]
    hits: int = 0


class CacheStorage:
    """Provides caching capabilities for analysis results"""
    
    def __init__(self, cache_dir: Path, ttl_hours: int = 24):
        self.cache_dir = cache_dir
        self.ttl_hours = ttl_hours
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._memory_cache: Dict[str, CacheEntry] = {}
    
    def get(self, key: str, use_memory: bool = True) -> Optional[Any]:
        """
        Get value from cache
        
        Args:
            key: Cache key
            use_memory: Whether to check memory cache first
        """
        # Check memory cache first
        if use_memory and key in self._memory_cache:
            entry = self._memory_cache[key]
            
            if self._is_expired(entry):
                del self._memory_cache[key]
                return None
            
            entry.hits += 1
            return entry.value
        
        # Check file cache
        cache_file = self._get_cache_file(key)
        if not cache_file.exists():
            return None
        
        try:
            with open(cache_file, 'rb') as f:
                entry = pickle.load(f)
            
            if self._is_expired(entry):
                cache_file.unlink()
                return None
            
            # Load into memory cache
            if use_memory:
                self._memory_cache[key] = entry
            
            entry.hits += 1
            return entry.value
        except Exception:
            return None
    
    def set(self, key: str, value: Any, 
            ttl_hours: Optional[int] = None,
            use_memory: bool = True) -> bool:
        """
        Set value in cache
        
        Args:
            key: Cache key
            value: Value to cache
            ttl_hours: Custom TTL in hours (uses default if None)
            use_memory: Whether to also store in memory
        """
        try:
            ttl = ttl_hours if ttl_hours is not None else self.ttl_hours
            expires_at = datetime.now() + timedelta(hours=ttl)
            
            entry = CacheEntry(
                key=key,
                value=value,
                created_at=datetime.now(),
                expires_at=expires_at
            )
            
            # Save to file
            cache_file = self._get_cache_file(key)
            with open(cache_file, 'wb') as f:
                pickle.dump(entry, f)
            
            # Save to memory
            if use_memory:
                self._memory_cache[key] = entry
            
            return True
        except Exception:
            return False
    
    def delete(self, key: str) -> bool:
        """Delete item from cache"""
        # Remove from memory
        if key in self._memory_cache:
            del self._memory_cache[key]
        
        # Remove from file
        cache_file = self._get_cache_file(key)
        if cache_file.exists():
            try:
                cache_file.unlink()
                return True
            except Exception:
                return False
        
        return True
    
    def clear(self) -> bool:
        """Clear all cache"""
        try:
            # Clear memory
            self._memory_cache.clear()
            
            # Clear files
            for cache_file in self.cache_dir.glob('*.cache'):
                cache_file.unlink()
            
            return True
        except Exception:
            return False
    
    def cleanup_expired(self) -> int:
        """Remove expired cache entries"""
        removed = 0
        
        # Clean memory cache
        expired_keys = [
            key for key, entry in self._memory_cache.items()
            if self._is_expired(entry)
        ]
        for key in expired_keys:
            del self._memory_cache[key]
            removed += 1
        
        # Clean file cache
        for cache_file in self.cache_dir.glob('*.cache'):
            try:
                with open(cache_file, 'rb') as f:
                    entry = pickle.load(f)
                
                if self._is_expired(entry):
                    cache_file.unlink()
                    removed += 1
            except Exception:
                continue
        
        return removed
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_entries = len(self._memory_cache) + len(list(self.cache_dir.glob('*.cache')))
        total_hits = sum(entry.hits for entry in self._memory_cache.values())
        
        return {
            'total_entries': total_entries,
            'memory_entries': len(self._memory_cache),
            'file_entries': len(list(self.cache_dir.glob('*.cache'))),
            'total_hits': total_hits,
            'cache_dir': str(self.cache_dir)
        }
    
    def _get_cache_file(self, key: str) -> Path:
        """Get cache file path for key"""
        safe_key = key.replace('/', '_').replace('\\', '_')
        return self.cache_dir / f"{safe_key}.cache"
    
    def _is_expired(self, entry: CacheEntry) -> bool:
        """Check if cache entry is expired"""
        if entry.expires_at is None:
            return False
        return datetime.now() > entry.expires_at
# =============================================================================
# src/infrastructure/persistence/json_serializer.py
# =============================================================================
"""JSON Serializer - Serializes domain entities to/from JSON"""

import json
from pathlib import Path
from typing import Any, Dict, List
from datetime import datetime
from enum import Enum


class JSONSerializer:
    """Handles serialization of domain entities to JSON"""
    
    @staticmethod
    def serialize(obj: Any) -> str:
        """Serialize object to JSON string"""
        return json.dumps(
            obj,
            default=JSONSerializer._default_serializer,
            indent=2,
            ensure_ascii=False
        )
    
    @staticmethod
    def deserialize(json_str: str) -> Any:
        """Deserialize JSON string to object"""
        return json.loads(json_str)
    
    @staticmethod
    def serialize_to_file(obj: Any, file_path: Path) -> bool:
        """Serialize object and save to file"""
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(
                    obj,
                    f,
                    default=JSONSerializer._default_serializer,
                    indent=2,
                    ensure_ascii=False
                )
            return True
        except Exception:
            return False
    
    @staticmethod
    def deserialize_from_file(file_path: Path) -> Any:
        """Load and deserialize object from file"""
        if not file_path.exists():
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return None
    
    @staticmethod
    def serialize_list(objects: List[Any]) -> str:
        """Serialize list of objects"""
        return JSONSerializer.serialize(objects)
    
    @staticmethod
    def serialize_dict(data: Dict[str, Any]) -> str:
        """Serialize dictionary"""
        return JSONSerializer.serialize(data)
    
    @staticmethod
    def _default_serializer(obj: Any) -> Any:
        """Handle special types during serialization"""
        # Handle datetime
        if isinstance(obj, datetime):
            return obj.isoformat()
        
        # Handle Path
        if isinstance(obj, Path):
            return str(obj)
        
        # Handle Enum
        if isinstance(obj, Enum):
            return obj.value
        
        # Handle objects with to_dict method
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        
        # Handle dataclasses
        if hasattr(obj, '__dataclass_fields__'):
            return {
                field: getattr(obj, field)
                for field in obj.__dataclass_fields__
            }
        
        # Fallback to string representation
        return str(obj)
    
    @staticmethod
    def pretty_print(obj: Any) -> str:
        """Pretty print object as JSON"""
        return json.dumps(
            obj,
            default=JSONSerializer._default_serializer,
            indent=4,
            sort_keys=True,
            ensure_ascii=False
        )
    
    @staticmethod
    def minify(json_str: str) -> str:
        """Minify JSON string (remove whitespace)"""
        obj = json.loads(json_str)
        return json.dumps(obj, separators=(',', ':'))
    
    @staticmethod
    def validate_json(json_str: str) -> bool:
        """Validate if string is valid JSON"""
        try:
            json.loads(json_str)
            return True
        except json.JSONDecodeError:
            return False
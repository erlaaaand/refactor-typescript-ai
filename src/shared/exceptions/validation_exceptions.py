# =============================================================================
# src/shared/exceptions/validation_exceptions.py
# =============================================================================
"""Validation-specific Exceptions"""

from typing import Any, Dict, Optional
from .base_exceptions import ValidationException as BaseValidationException


class ConfigValidationException(BaseValidationException):
    """Raised when configuration validation fails"""
    
    def __init__(self, message: str, config_key: str = "", 
                 expected: Any = None, actual: Any = None):
        self.config_key = config_key
        self.expected = expected
        self.actual = actual
        
        details = {'config_key': config_key}
        if expected is not None:
            details['expected'] = expected
        if actual is not None:
            details['actual'] = actual
        
        super().__init__(message, details)


class SchemaValidationException(BaseValidationException):
    """Raised when schema validation fails"""
    
    def __init__(self, message: str, schema_path: str = "",
                 validation_errors: Optional[list] = None):
        self.schema_path = schema_path
        self.validation_errors = validation_errors or []
        
        details = {
            'schema_path': schema_path,
            'error_count': len(self.validation_errors)
        }
        
        super().__init__(message, details)


class FileValidationException(BaseValidationException):
    """Raised when file validation fails"""
    
    def __init__(self, message: str, file_path: str = "",
                 validation_type: str = ""):
        self.file_path = file_path
        self.validation_type = validation_type
        
        details = {
            'file_path': file_path,
            'validation_type': validation_type
        }
        
        super().__init__(message, details)


class PathValidationException(BaseValidationException):
    """Raised when path validation fails"""
    
    def __init__(self, message: str, path: str = "",
                 reason: str = ""):
        self.path = path
        self.reason = reason
        
        details = {
            'path': path,
            'reason': reason
        }
        
        super().__init__(message, details)


class ValueRangeException(BaseValidationException):
    """Raised when value is out of valid range"""
    
    def __init__(self, message: str, value: Any, 
                 min_value: Any = None, max_value: Any = None):
        self.value = value
        self.min_value = min_value
        self.max_value = max_value
        
        details = {'value': value}
        if min_value is not None:
            details['min'] = min_value
        if max_value is not None:
            details['max'] = max_value
        
        super().__init__(message, details)


class RequiredFieldException(BaseValidationException):
    """Raised when required field is missing"""
    
    def __init__(self, field_name: str, object_type: str = ""):
        self.field_name = field_name
        self.object_type = object_type
        
        message = f"Required field missing: {field_name}"
        if object_type:
            message += f" in {object_type}"
        
        details = {
            'field_name': field_name,
            'object_type': object_type
        }
        
        super().__init__(message, details)


class TypeValidationException(BaseValidationException):
    """Raised when value type is incorrect"""
    
    def __init__(self, message: str, expected_type: type,
                 actual_type: type, value: Any = None):
        self.expected_type = expected_type
        self.actual_type = actual_type
        self.value = value
        
        details = {
            'expected_type': expected_type.__name__,
            'actual_type': actual_type.__name__
        }
        
        super().__init__(message, details)
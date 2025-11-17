# =============================================================================
# src/interfaces/config/config_validator.py
# =============================================================================
"""Configuration Validator - Validates configuration files"""

from typing import Dict, Any, List
from pathlib import Path
from ...shared.exceptions.base_exceptions import ValidationException


class ConfigValidator:
    """Validates configuration against schema"""
    
    REQUIRED_FIELDS = {
        'project': ['name', 'version'],
        'scanning': ['root_directory'],
        'thresholds': ['complexity', 'quality', 'refactoring']
    }
    
    VALID_LOG_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    VALID_OUTPUT_FORMATS = ['json', 'yaml', 'html', 'markdown']
    
    @staticmethod
    def validate(config: Dict[str, Any]) -> bool:
        """
        Validate complete configuration
        
        Args:
            config: Configuration dictionary
            
        Returns:
            True if valid
            
        Raises:
            ValidationException: If validation fails
        """
        ConfigValidator._validate_structure(config)
        ConfigValidator._validate_project(config.get('project', {}))
        ConfigValidator._validate_scanning(config.get('scanning', {}))
        ConfigValidator._validate_thresholds(config.get('thresholds', {}))
        ConfigValidator._validate_output(config.get('output', {}))
        ConfigValidator._validate_logging(config.get('logging', {}))
        
        return True
    
    @staticmethod
    def _validate_structure(config: Dict[str, Any]):
        """Validate top-level structure"""
        for section, fields in ConfigValidator.REQUIRED_FIELDS.items():
            if section not in config:
                raise ValidationException(
                    f"Missing required section: {section}",
                    {'section': section}
                )
            
            section_config = config[section]
            for field in fields:
                if field not in section_config:
                    raise ValidationException(
                        f"Missing required field in {section}: {field}",
                        {'section': section, 'field': field}
                    )
    
    @staticmethod
    def _validate_project(project: Dict[str, Any]):
        """Validate project configuration"""
        if not project.get('name'):
            raise ValidationException("Project name cannot be empty")
        
        version = project.get('version', '')
        if not ConfigValidator._is_valid_version(version):
            raise ValidationException(
                "Invalid version format (expected: X.Y.Z)",
                {'version': version}
            )
    
    @staticmethod
    def _validate_scanning(scanning: Dict[str, Any]):
        """Validate scanning configuration"""
        root_dir = scanning.get('root_directory')
        if root_dir and not Path(root_dir).exists():
            raise ValidationException(
                "Root directory does not exist",
                {'path': root_dir}
            )
        
        max_workers = scanning.get('max_workers', 4)
        if not isinstance(max_workers, int) or not 1 <= max_workers <= 16:
            raise ValidationException(
                "max_workers must be between 1 and 16",
                {'value': max_workers}
            )
        
        max_file_size = scanning.get('max_file_size_mb', 5)
        if not isinstance(max_file_size, (int, float)) or max_file_size <= 0:
            raise ValidationException(
                "max_file_size_mb must be positive",
                {'value': max_file_size}
            )
    
    @staticmethod
    def _validate_thresholds(thresholds: Dict[str, Any]):
        """Validate threshold configuration"""
        # Validate complexity thresholds
        complexity = thresholds.get('complexity', {})
        simple_max = complexity.get('simple_max', 30)
        medium_max = complexity.get('medium_max', 60)
        
        if simple_max >= medium_max:
            raise ValidationException(
                "simple_max must be less than medium_max",
                {'simple_max': simple_max, 'medium_max': medium_max}
            )
        
        # Validate quality thresholds
        quality = thresholds.get('quality', {})
        excellent = quality.get('excellent_min', 80)
        good = quality.get('good_min', 60)
        fair = quality.get('fair_min', 40)
        
        if not (fair < good < excellent):
            raise ValidationException(
                "Quality thresholds must be: fair < good < excellent",
                {'fair': fair, 'good': good, 'excellent': excellent}
            )
    
    @staticmethod
    def _validate_output(output: Dict[str, Any]):
        """Validate output configuration"""
        formats = output.get('formats', [])
        if formats:
            for fmt in formats:
                if fmt not in ConfigValidator.VALID_OUTPUT_FORMATS:
                    raise ValidationException(
                        f"Invalid output format: {fmt}",
                        {'valid_formats': ConfigValidator.VALID_OUTPUT_FORMATS}
                    )
    
    @staticmethod
    def _validate_logging(logging: Dict[str, Any]):
        """Validate logging configuration"""
        level = logging.get('level', 'INFO')
        if level not in ConfigValidator.VALID_LOG_LEVELS:
            raise ValidationException(
                f"Invalid log level: {level}",
                {'valid_levels': ConfigValidator.VALID_LOG_LEVELS}
            )
    
    @staticmethod
    def _is_valid_version(version: str) -> bool:
        """Check if version follows semantic versioning"""
        import re
        pattern = r'^\d+\.\d+\.\d+$'
        return bool(re.match(pattern, version))
    
    @staticmethod
    def get_validation_errors(config: Dict[str, Any]) -> List[str]:
        """
        Get all validation errors without raising exception
        
        Returns:
            List of error messages
        """
        errors = []
        
        try:
            ConfigValidator.validate(config)
        except ValidationException as e:
            errors.append(e.message)
        
        return errors
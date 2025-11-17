# =============================================================================
# src/interfaces/config/config_loader.py
# =============================================================================
"""Configuration Loader"""

from pathlib import Path
from typing import Dict, Any, Optional
import yaml
import json

class ConfigLoader:
    """Loads and manages application configuration"""
    
    DEFAULT_CONFIG_PATH = Path("config/config.yaml")
    
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or self.DEFAULT_CONFIG_PATH
        self._config: Dict[str, Any] = {}
        self._loaded = False
    
    def load(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            self._config = yaml.safe_load(f)
        
        self._loaded = True
        return self._config
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key (supports dot notation)"""
        if not self._loaded:
            self.load()
        
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_scanning_config(self) -> Dict[str, Any]:
        """Get scanning configuration"""
        return self.get('scanning', {})
    
    def get_thresholds(self) -> Dict[str, Any]:
        """Get threshold configuration"""
        return self.get('thresholds', {})
    
    def get_output_config(self) -> Dict[str, Any]:
        """Get output configuration"""
        return self.get('output', {})
    
    def get_complexity_weights(self) -> Dict[str, Any]:
        """Get complexity weights"""
        return self.get('complexity_weights', {})
    
    def get_refactoring_strategies(self) -> Dict[str, Any]:
        """Get refactoring strategies"""
        return self.get('refactoring.strategies', {})
    
    def save(self, output_path: Optional[Path] = None):
        """Save configuration to file"""
        if output_path is None:
            output_path = self.config_path
        
        with open(output_path, 'w') as f:
            yaml.dump(self._config, f, default_flow_style=False, indent=2)
    
    def update(self, key: str, value: Any):
        """Update configuration value"""
        if not self._loaded:
            self.load()
        
        keys = key.split('.')
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def to_dict(self) -> Dict[str, Any]:
        """Get configuration as dictionary"""
        if not self._loaded:
            self.load()
        return self._config.copy()
    
    def to_json(self, output_path: Path):
        """Export configuration as JSON"""
        if not self._loaded:
            self.load()
        
        with open(output_path, 'w') as f:
            json.dump(self._config, f, indent=2)
    
    @staticmethod
    def create_default_config(output_path: Path) -> 'ConfigLoader':
        """Create default configuration file"""
        default_config = {
            'project': {
                'name': 'test-refactor-ai',
                'version': '2.1.0'
            },
            'scanning': {
                'root_directory': 'backend/src',
                'max_workers': 4,
                'exclude_dirs': ['node_modules', 'dist', 'build']
            },
            'thresholds': {
                'complexity': {
                    'simple_max': 30,
                    'medium_max': 60,
                    'complex_min': 60
                }
            }
        }
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            yaml.dump(default_config, f, default_flow_style=False)
        
        return ConfigLoader(output_path)
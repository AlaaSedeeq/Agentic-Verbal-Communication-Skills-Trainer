import yaml
from typing import Dict, Any, Iterator

from .logger import logger

class ConfigBase:
    """Enhanced ConfigBase with iteration support"""
    
    def __init__(self, dictionary: Dict[str, Any]):
        self._raw_dict = dictionary  # Store original dictionary
        for key, value in dictionary.items():
            if isinstance(value, dict):
                setattr(self, key, ConfigBase(value))
            else:
                setattr(self, key, value)
    
    def __iter__(self) -> Iterator:
        """Make ConfigBase iterable"""
        return iter(self._raw_dict)
    
    def items(self):
        """Support dict-like items() method"""
        return self._raw_dict.items()
    
    def get(self, key, default=None):
        """Support dict-like get() method"""
        return self._raw_dict.get(key, default)
    
    def __getitem__(self, key):
        """Support dictionary-style access"""
        return getattr(self, key)
    
    def __str__(self) -> str:
        return str(self._raw_dict)
    
    def to_dict(self) -> Dict:
        """Convert back to dictionary"""
        return self._raw_dict

def load_config(path_to_yaml: str = "config/config.yaml") -> ConfigBase:
    """Load YAML configuration file"""
    try:
        with open(path_to_yaml, 'r', encoding='utf-8') as yaml_file:
            content = yaml.safe_load(yaml_file)
            config = ConfigBase(content)
            logger.info(f"Config loaded successfully: {path_to_yaml}")
            return config
    except Exception as e:
        logger.error(f"Error loading config: {e}")
        raise

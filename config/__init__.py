"""Configuration manager untuk semua outlet"""
from typing import Dict, Optional
from .base_config import OutletConfig
from .waruna_config import get_waruna_config
from .papper_lunch_config import get_papper_lunch_config
from .song_fa_config import get_song_fa_config

class ConfigManager:
    """Manager untuk semua konfigurasi outlet"""
    
    def __init__(self):
        self.outlets: Dict[str, OutletConfig] = {}
        self._load_configs()
    
    def _load_configs(self):
        """Load semua konfigurasi outlet"""
        self.outlets['waruna'] = get_waruna_config()
        self.outlets['papper_lunch'] = get_papper_lunch_config()
        self.outlets['song_fa'] = get_song_fa_config()
    
    def get_outlet(self, name: str) -> Optional[OutletConfig]:
        """Get outlet configuration by name"""
        return self.outlets.get(name)
    
    def get_all_outlets(self) -> Dict[str, OutletConfig]:
        """Get all outlet configurations"""
        return self.outlets
    
    def get_outlet_names(self) -> list:
        """Get list of outlet names"""
        return list(self.outlets.keys())
    
    def get_outlet_display_names(self) -> Dict[str, str]:
        """Get display names for all outlets"""
        return {name: outlet.display_name for name, outlet in self.outlets.items()}

# Singleton instance
_config_manager = None

def get_config_manager() -> ConfigManager:
    """Get or create config manager singleton"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager

def init_outlet_tables(db_manager):
    """Initialize semua tables untuk semua outlet"""
    config_manager = get_config_manager()
    
    for outlet_name, outlet_config in config_manager.get_all_outlets().items():
        for module in outlet_config.modules:
            # Create table if not exists
            db_manager.create_table(outlet_name, module.table_name, module.columns)
    
    return True
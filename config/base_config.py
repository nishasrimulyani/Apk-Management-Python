"""Base configuration untuk semua outlet"""

from typing import Dict, List, Optional

class ModuleConfig:
    """Configuration for a module"""
    
    def __init__(self, name: str, icon: str, table_name: str, columns: List[Dict], date_field: Optional[str] = None, chart_config: Optional[Dict] = None):
        self.name = name
        self.icon = icon
        self.table_name = table_name
        self.columns = columns
        self.date_field = date_field
        self.chart_config = chart_config or {}

class OutletConfig:
    """Configuration for an outlet"""
    
    def __init__(self, name: str, display_name: str, icon: str, modules: List[ModuleConfig]):
        self.name = name
        self.display_name = display_name
        self.icon = icon
        self.modules = modules
    
    def get_module(self, module_name: str) -> Optional[ModuleConfig]:
        """Get module by name"""
        for module in self.modules:
            if module.name == module_name:
                return module
        return None
    
    def get_table_names(self) -> List[str]:
        """Get all table names"""
        return [f"{self.name}_{m.table_name}" for m in self.modules]

# Column types helper
def text_column(name: str, label: str, default: str = "") -> Dict:
    return {'name': name, 'label': label, 'type': 'text', 'default': default}

def number_column(name: str, label: str) -> Dict:
    return {'name': name, 'label': label, 'type': 'number'}

def date_column(name: str, label: str) -> Dict:
    return {'name': name, 'label': label, 'type': 'date'}

def select_column(name: str, label: str, options: List[str]) -> Dict:
    return {'name': name, 'label': label, 'type': 'select', 'options': options}

def textarea_column(name: str, label: str) -> Dict:
    return {'name': name, 'label': label, 'type': 'textarea'}

def computed_column(name: str, label: str) -> Dict:
    return {'name': name, 'label': label, 'type': 'computed'}
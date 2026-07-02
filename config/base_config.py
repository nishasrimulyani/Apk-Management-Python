"""Base configuration untuk semua outlet dan manager pusat"""

from typing import Dict, List, Optional

class ModuleConfig:
    """Konfigurasi untuk modul kerja spesifik (misal: Penjualan, Stok)"""
    def __init__(self, name: str, icon: str, table_name: str, columns: List[Dict], date_field: Optional[str] = None, chart_config: Optional[Dict] = None):
        self.name = name
        self.icon = icon
        self.table_name = table_name
        self.columns = columns
        self.date_field = date_field
        self.chart_config = chart_config or {}

class OutletConfig:
    """Konfigurasi untuk satu brand / cabang outlet"""
    def __init__(self, name: str, display_name: str, icon: str, modules: List[ModuleConfig]):
        self.name = name
        self.display_name = display_name
        self.icon = icon
        self.modules = modules
    
    def get_module(self, module_name: str) -> Optional[ModuleConfig]:
        """Mendapatkan objek modul berdasarkan namanya"""
        for module in self.modules:
            if module.name == module_name:
                return module
        return None
    
    def get_table_names(self) -> List[str]:
        """Mendapatkan nama tabel gabungan unik untuk SQLite"""
        return [f"{self.name}_{m.table_name}" for m in self.modules]


class AppConfigManager:
    """Pusat management yang mengatur seluruh outlet (Dibutuhkan oleh file utama)"""
    def __init__(self):
        self.outlets: Dict[str, OutletConfig] = {}
        self._register_outlets()

    def _register_outlets(self):
        """
        Tempat mendaftarkan brand/outlet Anda secara data-driven.
        Contoh di bawah mendaftarkan 'Waruna' dan 'Papper Lunch'.
        """
        # --- CONTOH OUTLET 1: WARUNA ---
        waruna_modules = [
            ModuleConfig(
                name="Penjualan Harian",
                icon="💰",
                table_name="penjualan",
                columns=[
                    date_column("tanggal", "Tanggal Transaksi"),
                    text_column("produk", "Nama Menu / Produk"),
                    number_column("total_harga", "Total Pendapatan (Rp)"),
                    select_column("pembayaran", "Metode Pembayaran", ["Cash", "QRIS", "Transfer"])
                ],
                chart_config={
                    "type": ["bar", "line", "pie"],
                    "metrics": [{"field": "total_harga", "label": "Total Penjualan"}],
                    "group_by": "pembayaran"
                }
            )
        ]
        self.outlets["waruna"] = OutletConfig("waruna", "Waruna", "🍲", waruna_modules)

        # --- CONTOH OUTLET 2: PAPPER LUNCH ---
        papper_modules = [
            ModuleConfig(
                name="Stok Bahan Baku",
                icon="🥩",
                table_name="stok_bahan",
                columns=[
                    date_column("tanggal_cek", "Tanggal Pengecekan"),
                    text_column("bahan", "Nama Bahan Baku"),
                    number_column("jumlah", "Jumlah Masuk (Kg)"),
                    textarea_column("keterangan", "Catatan Kondisi")
                ],
                chart_config={
                    "type": ["bar"],
                    "metrics": [{"field": "jumlah", "label": "Volume Bahan"}],
                    "group_by": "bahan"
                }
            )
        ]
        self.outlets["papper_lunch"] = OutletConfig("papper_lunch", "Papper Lunch", "🍳", papper_modules)

    def get_outlet_display_names(self) -> Dict[str, str]:
        """Mengembalikan dict berisi key asli dan display name untuk selectbox Streamlit"""
        return {name: config.display_name for name, config in self.outlets.items()}

    def get_outlet(self, name: str) -> Optional[OutletConfig]:
        """Mengambil objek konfigurasi outlet berdasarkan key-nya"""
        return self.outlets.get(name)


# ==================== COLUMN TYPES HELPER ====================

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
"""Waruna Outlet Configuration"""
from .base_config import *

def get_waruna_config() -> OutletConfig:
    """Get Waruna outlet configuration"""
    
    modules = [
        ModuleConfig(
            name="CSO Waruna",
            icon="👨‍💼",
            table_name="cso_waruna",
            date_field="tanggal",
            columns=[
                date_column("tanggal", "Tanggal"),
                text_column("nama_cso", "Nama CSO"),
                text_column("outlet", "Outlet"),
                number_column("target_penjualan", "Target Penjualan (Rp)"),
                number_column("realisasi_penjualan", "Realisasi Penjualan (Rp)"),
                number_column("target_kunjungan", "Target Kunjungan"),
                number_column("realisasi_kunjungan", "Realisasi Kunjungan"),
                select_column("status", "Status", ['Belum', 'Proses', 'Selesai', 'Tunda']),
                textarea_column("keterangan", "Keterangan")
            ],
            chart_config={
                'type': ['bar', 'line', 'area'],
                'metrics': [
                    {'field': 'target_penjualan', 'label': 'Target Penjualan'},
                    {'field': 'realisasi_penjualan', 'label': 'Realisasi Penjualan'},
                    {'field': 'target_kunjungan', 'label': 'Target Kunjungan'},
                    {'field': 'realisasi_kunjungan', 'label': 'Realisasi Kunjungan'}
                ],
                'group_by': 'nama_cso',
                'category': 'status'
            }
        ),
        ModuleConfig(
            name="Makan Karyawan",
            icon="🍽️",
            table_name="makan_karyawan",
            date_field="tanggal",
            columns=[
                date_column("tanggal", "Tanggal"),
                select_column("shift", "Shift", ['Pagi', 'Siang', 'Malam', 'All Shift']),
                number_column("jumlah_karyawan", "Jumlah Karyawan"),
                text_column("menu_makanan", "Menu Makanan"),
                number_column("total_biaya", "Total Biaya (Rp)"),
                text_column("pic_dapur", "PIC Dapur"),
                textarea_column("keterangan", "Keterangan")
            ]
        ),
        ModuleConfig(
            name="Produksi Kitchen & BAR",
            icon="👨‍🍳",
            table_name="produksi_kitchen",
            date_field="tanggal",
            columns=[
                date_column("tanggal", "Tanggal"),
                select_column("departemen", "Departemen", ['Kitchen', 'BAR', 'Pastry', 'All']),
                text_column("item_produksi", "Item Produksi"),
                number_column("target_produksi", "Target Produksi"),
                number_column("realisasi_produksi", "Realisasi Produksi"),
                textarea_column("bahan_baku", "Bahan Baku"),
                text_column("chef_pic", "Chef/PIC"),
                select_column("status", "Status", ['Proses', 'Selesai', 'Tunda', 'Cancel'])
            ]
        ),
        ModuleConfig(
            name="Waste Kitchen & BAR",
            icon="🗑️",
            table_name="waste_kitchen",
            date_field="tanggal",
            columns=[
                date_column("tanggal", "Tanggal"),
                select_column("jenis_waste", "Jenis Waste", ['Makanan', 'Minuman', 'Bahan Baku', 'Lainnya']),
                select_column("departemen", "Departemen", ['Kitchen', 'BAR', 'Pastry']),
                text_column("item_waste", "Item Waste"),
                number_column("jumlah_waste", "Jumlah Waste"),
                select_column("satuan", "Satuan", ['Porsi', 'Kg', 'Liter', 'Pcs', 'Box']),
                textarea_column("penyebab", "Penyebab"),
                number_column("estimasi_kerugian", "Estimasi Kerugian (Rp)"),
                textarea_column("tindakan_perbaikan", "Tindakan Perbaikan")
            ]
        ),
        # ... Modul Waruna lainnya (dari kode sebelumnya)
    ]
    
    return OutletConfig(
        name="waruna",
        display_name="Waruna",
        icon="🏪",
        modules=modules
    )
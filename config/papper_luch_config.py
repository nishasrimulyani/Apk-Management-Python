"""Papper Lunch Outlet Configuration"""
from .base_config import *

def get_papper_lunch_config() -> OutletConfig:
    """Get Papper Lunch outlet configuration"""
    
    modules = [
        # 1. Rekap Waste Mingguan/Bulanan
        ModuleConfig(
            name="Rekap Waste (Mingguan/Bulanan)",
            icon="🗑️",
            table_name="waste_periodik",
            date_field="tanggal",
            columns=[
                date_column("tanggal", "Tanggal"),
                select_column("periode", "Periode", ['Mingguan', 'Bulanan']),
                number_column("minggu_ke", "Minggu Ke-"),
                select_column("bulan", "Bulan", [
                    'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
                    'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'
                ]),
                number_column("tahun", "Tahun"),
                select_column("kategori", "Kategori Waste", [
                    'Makanan Jadi', 'Bahan Baku', 'Minuman', 'Kemasan', 'Lainnya'
                ]),
                text_column("item_waste", "Item Waste"),
                number_column("jumlah_waste", "Jumlah Waste"),
                select_column("satuan", "Satuan", ['Kg', 'Porsi', 'Liter', 'Pcs', 'Box']),
                number_column("total_kerugian", "Total Kerugian (Rp)"),
                textarea_column("penyebab", "Penyebab Waste"),
                textarea_column("tindakan", "Tindakan Pencegahan"),
                text_column("pic", "PIC")
            ],
            chart_config={
                'type': ['bar', 'line', 'pie'],
                'metrics': [
                    {'field': 'jumlah_waste', 'label': 'Jumlah Waste'},
                    {'field': 'total_kerugian', 'label': 'Total Kerugian'}
                ],
                'group_by': 'kategori',
                'category': 'periode'
            }
        ),
        
        # 2. Rekap Waste Format ESB
        ModuleConfig(
            name="Rekap Waste Format ESB",
            icon="📊",
            table_name="waste_esb",
            date_field="tanggal",
            columns=[
                date_column("tanggal", "Tanggal"),
                text_column("no_esb", "No. ESB"),
                select_column("departemen", "Departemen", ['Kitchen', 'Service', 'Bar', 'Storage']),
                text_column("item_name", "Nama Item"),
                text_column("item_code", "Kode Item"),
                number_column("quantity", "Quantity"),
                select_column("unit", "Unit", ['Kg', 'Gram', 'Liter', 'Pcs', 'Box', 'Pack']),
                number_column("harga_satuan", "Harga Satuan (Rp)"),
                number_column("total_harga", "Total Harga (Rp)"),
                select_column("kategori_waste", "Kategori Waste ESB", [
                    'Expired', 'Over Production', 'Quality Issue', 'Customer Return', 'Other'
                ]),
                textarea_column("keterangan", "Keterangan"),
                text_column("approved_by", "Approved By"),
                date_column("tanggal_approve", "Tanggal Approve")
            ],
            chart_config={
                'type': ['bar', 'pie', 'treemap'],
                'metrics': [
                    {'field': 'quantity', 'label': 'Quantity'},
                    {'field': 'total_harga', 'label': 'Total Harga'}
                ],
                'group_by': 'kategori_waste',
                'category': 'departemen'
            }
        ),
        
        # 3. Rekap Foodblogger Papper Lunch
        ModuleConfig(
            name="Foodblogger / Influencer Report",
            icon="📸",
            table_name="foodblogger_pl",
            date_field="tanggal_kunjungan",
            columns=[
                date_column("tanggal_kunjungan", "Tanggal Kunjungan"),
                text_column("nama_influencer", "Nama Influencer"),
                select_column("platform", "Platform", [
                    'Instagram', 'TikTok', 'YouTube', 'Twitter/X', 'Blog', 'Lainnya'
                ]),
                number_column("followers", "Jumlah Followers"),
                text_column("konten_type", "Tipe Konten"),
                select_column("jenis_collab", "Jenis Collab", [
                    'Paid Promote', 'Barter', 'Invitation', 'Review', 'Event'
                ]),
                number_column("biaya_collab", "Biaya Collab (Rp)"),
                textarea_column("menu_dicoba", "Menu yang Dicoba"),
                number_column("rating", "Rating (1-5)"),
                textarea_column("review", "Review / Feedback"),
                text_column("link_post", "Link Post"),
                number_column("engagement_rate", "Engagement Rate (%)"),
                number_column("reach", "Reach"),
                select_column("status", "Status", ['Draft', 'Published', 'Pending', 'Rejected']),
                text_column("pic_marketing", "PIC Marketing")
            ],
            chart_config={
                'type': ['bar', 'pie', 'scatter'],
                'metrics': [
                    {'field': 'followers', 'label': 'Followers'},
                    {'field': 'biaya_collab', 'label': 'Biaya Collab'},
                    {'field': 'rating', 'label': 'Rating'},
                    {'field': 'engagement_rate', 'label': 'Engagement Rate'}
                ],
                'group_by': 'platform',
                'category': 'jenis_collab'
            }
        ),
        
        # 4. Sales Daily, Menu & Detail
        ModuleConfig(
            name="Sales Daily, Menu & Detail",
            icon="💰",
            table_name="sales_detail_pl",
            date_field="tanggal",
            columns=[
                date_column("tanggal", "Tanggal"),
                select_column("shift", "Shift", ['Pagi', 'Siang', 'Malam']),
                select_column("kategori_menu", "Kategori Menu", [
                    'Main Course', 'Appetizer', 'Dessert', 'Minuman', 'Promo Package', 'Add On'
                ]),
                text_column("nama_menu", "Nama Menu"),
                text_column("menu_code", "Kode Menu"),
                number_column("harga_satuan", "Harga Satuan (Rp)"),
                number_column("jumlah_terjual", "Jumlah Terjual"),
                number_column("total_penjualan", "Total Penjualan (Rp)"),
                number_column("diskon_per_item", "Diskon Per Item (Rp)"),
                number_column("net_sales", "Net Sales (Rp)"),
                select_column("metode_pembayaran", "Metode Pembayaran", [
                    'Tunai', 'QRIS', 'Kartu Kredit', 'Debit', 'GoPay', 'ShopeePay'
                ]),
                select_column("jenis_order", "Jenis Order", ['Dine In', 'Take Away', 'Delivery', 'Online Order']),
                text_column("kasir", "Kasir"),
                textarea_column("notes", "Notes")
            ],
            chart_config={
                'type': ['bar', 'line', 'pie', 'treemap'],
                'metrics': [
                    {'field': 'total_penjualan', 'label': 'Total Penjualan'},
                    {'field': 'net_sales', 'label': 'Net Sales'},
                    {'field': 'jumlah_terjual', 'label': 'Jumlah Terjual'}
                ],
                'group_by': 'kategori_menu',
                'category': 'metode_pembayaran'
            }
        ),
        
        # 5. Stock Movement Report
        ModuleConfig(
            name="Stock Movement Report",
            icon="📦",
            table_name="stock_movement_pl",
            date_field="tanggal",
            columns=[
                date_column("tanggal", "Tanggal"),
                text_column("item_name", "Nama Item"),
                text_column("item_code", "Kode Item"),
                select_column("kategori", "Kategori", [
                    'Bahan Baku', 'Bahan Packing', 'Minuman', 'Dry Stock', 'Peralatan'
                ]),
                number_column("stock_awal", "Stock Awal"),
                number_column("stock_masuk", "Stock Masuk"),
                number_column("stock_keluar", "Stock Keluar"),
                number_column("stock_akhir", "Stock Akhir"),
                select_column("jenis_movement", "Jenis Movement", [
                    'Pembelian', 'Produksi', 'Penjualan', 'Transfer', 'Adjustment', 'Waste'
                ]),
                textarea_column("keterangan", "Keterangan"),
                text_column("pic_gudang", "PIC Gudang"),
                select_column("status", "Status", [
                    'Pending', 'In Progress', 'Completed', 'Verified'
                ])
            ],
            chart_config={
                'type': ['bar', 'line', 'area'],
                'metrics': [
                    {'field': 'stock_awal', 'label': 'Stock Awal'},
                    {'field': 'stock_masuk', 'label': 'Stock Masuk'},
                    {'field': 'stock_keluar', 'label': 'Stock Keluar'},
                    {'field': 'stock_akhir', 'label': 'Stock Akhir'}
                ],
                'group_by': 'kategori',
                'category': 'jenis_movement'
            }
        ),
        
        # 6. Condiment PL Management
        ModuleConfig(
            name="Condiment PL Management",
            icon="🧂",
            table_name="condiment_pl",
            date_field="tanggal",
            columns=[
                date_column("tanggal", "Tanggal"),
                text_column("nama_condiment", "Nama Condiment"),
                text_column("kode_condiment", "Kode Condiment"),
                select_column("kategori", "Kategori", [
                    'Saus', 'Bumbu', 'Pelengkap', 'Minuman Pelengkap', 'Lainnya'
                ]),
                number_column("stock_minimal", "Stock Minimal"),
                number_column("stock_aktual", "Stock Aktual"),
                number_column("stock_digunakan", "Stock Digunakan Hari Ini"),
                number_column("kebutuhan_besok", "Kebutuhan Besok"),
                select_column("satuan", "Satuan", ['Botol', 'Sachet', 'Kg', 'Liter', 'Pcs']),
                select_column("status", "Status", [
                    'Stock Cukup', 'Stock Menipis', 'Perlu Re-order', 'Habis'
                ]),
                number_column("harga_satuan", "Harga Satuan (Rp)"),
                number_column("total_nilai_stock", "Total Nilai Stock (Rp)"),
                textarea_column("keterangan", "Keterangan"),
                text_column("pic", "PIC")
            ],
            chart_config={
                'type': ['bar', 'pie', 'treemap'],
                'metrics': [
                    {'field': 'stock_aktual', 'label': 'Stock Aktual'},
                    {'field': 'kebutuhan_besok', 'label': 'Kebutuhan Besok'},
                    {'field': 'total_nilai_stock', 'label': 'Total Nilai Stock'}
                ],
                'group_by': 'kategori',
                'category': 'status'
            }
        ),
        
        # 7. Rekap Promo Diskon
        ModuleConfig(
            name="Rekap Promo & Diskon",
            icon="🏷️",
            table_name="promo_diskon_pl",
            date_field="tanggal_mulai",
            columns=[
                date_column("tanggal_mulai", "Tanggal Mulai"),
                date_column("tanggal_selesai", "Tanggal Selesai"),
                text_column("nama_promo", "Nama Promo"),
                text_column("kode_promo", "Kode Promo"),
                select_column("jenis_promo", "Jenis Promo", [
                    'Diskon Persen', 'Diskon Nominal', 'Buy 1 Get 1', 
                    'Bundle Package', 'Cashback', 'Voucher', 'Lainnya'
                ]),
                number_column("nilai_diskon", "Nilai Diskon (Rp)"),
                number_column("minimum_pembelian", "Minimum Pembelian (Rp)"),
                select_column("target_menu", "Target Menu", [
                    'Semua Menu', 'Menu Tertentu', 'Kategori Tertentu', 'Minimum Order'
                ]),
                number_column("jumlah_pengguna", "Jumlah Pengguna"),
                number_column("total_penjualan_promo", "Total Penjualan Promo (Rp)"),
                number_column("total_diskon_diberikan", "Total Diskon Diberikan (Rp)"),
                number_column("roi_promo", "ROI Promo (%)"),
                select_column("status", "Status", ['Aktif', 'Selesai', 'Akan Datang', 'Dihentikan']),
                textarea_column("hasil_evaluasi", "Hasil Evaluasi"),
                text_column("pic_marketing", "PIC Marketing")
            ],
            chart_config={
                'type': ['bar', 'pie', 'line'],
                'metrics': [
                    {'field': 'total_penjualan_promo', 'label': 'Total Penjualan'},
                    {'field': 'total_diskon_diberikan', 'label': 'Total Diskon'},
                    {'field': 'jumlah_pengguna', 'label': 'Jumlah Pengguna'},
                    {'field': 'roi_promo', 'label': 'ROI Promo'}
                ],
                'group_by': 'jenis_promo',
                'category': 'status'
            }
        )
    ]
    
    return OutletConfig(
        name="papper_lunch",
        display_name="Papper Lunch",
        icon="🥪",
        modules=modules
    )
"""Song Fa Outlet Configuration"""
from .base_config import *

def get_song_fa_config() -> OutletConfig:
    """Get Song Fa outlet configuration"""
    
    modules = [
        # 1. Rekap Waste Produk
        ModuleConfig(
            name="Rekap Waste Produk",
            icon="🗑️",
            table_name="waste_produk",
            date_field="tanggal",
            columns=[
                date_column("tanggal", "Tanggal"),
                select_column("kategori_produk", "Kategori Produk", [
                    'Bak Kut Teh', 'Bak Mua', 'Bak Chor Mee', 'Bak Laksa',
                    'Minuman', 'Side Dish', 'Lainnya'
                ]),
                text_column("nama_produk", "Nama Produk"),
                text_column("kode_produk", "Kode Produk"),
                number_column("jumlah_produksi", "Jumlah Produksi"),
                number_column("jumlah_terjual", "Jumlah Terjual"),
                number_column("jumlah_waste", "Jumlah Waste"),
                number_column("persentase_waste", "Persentase Waste (%)"),
                select_column("penyebab_waste", "Penyebab Waste", [
                    'Over Produksi', 'Kualitas Tidak Sesuai', 'Expired',
                    'Kesalahan Produksi', 'Penyimpanan', 'Lainnya'
                ]),
                number_column("harga_satuan", "Harga Satuan (Rp)"),
                number_column("total_kerugian", "Total Kerugian (Rp)"),
                textarea_column("tindakan_korektif", "Tindakan Korektif"),
                text_column("pic_produksi", "PIC Produksi"),
                select_column("status", "Status", ['Open', 'In Progress', 'Resolved', 'Closed'])
            ],
            chart_config={
                'type': ['bar', 'pie', 'line'],
                'metrics': [
                    {'field': 'jumlah_waste', 'label': 'Jumlah Waste'},
                    {'field': 'persentase_waste', 'label': 'Persentase Waste'},
                    {'field': 'total_kerugian', 'label': 'Total Kerugian'}
                ],
                'group_by': 'kategori_produk',
                'category': 'penyebab_waste'
            }
        ),
        
        # 2. Rekap Produksi Kitchen
        ModuleConfig(
            name="Rekap Produksi Kitchen",
            icon="👨‍🍳",
            table_name="produksi_kitchen_sf",
            date_field="tanggal_produksi",
            columns=[
                date_column("tanggal_produksi", "Tanggal Produksi"),
                select_column("shift", "Shift", ['Pagi', 'Siang', 'Malam']),
                select_column("kategori_produk", "Kategori Produk", [
                    'Bak Kut Teh', 'Bak Mua', 'Bak Chor Mee', 'Bak Laksa',
                    'Minuman', 'Side Dish', 'Dessert'
                ]),
                text_column("nama_produk", "Nama Produk"),
                number_column("target_produksi", "Target Produksi"),
                number_column("realisasi_produksi", "Realisasi Produksi"),
                number_column("selisih", "Selisih (+/-)"),
                number_column("persentase_capaian", "Persentase Capaian (%)"),
                textarea_column("bahan_baku_utama", "Bahan Baku Utama"),
                number_column("jumlah_bahan_baku", "Jumlah Bahan Baku"),
                textarea_column("catatan_produksi", "Catatan Produksi"),
                text_column("chef_pic", "Chef / PIC"),
                select_column("status_produksi", "Status Produksi", [
                    'Sesuai Target', 'Over Produksi', 'Under Produksi', 'Cancel'
                ])
            ],
            chart_config={
                'type': ['bar', 'line', 'area'],
                'metrics': [
                    {'field': 'target_produksi', 'label': 'Target Produksi'},
                    {'field': 'realisasi_produksi', 'label': 'Realisasi Produksi'},
                    {'field': 'persentase_capaian', 'label': 'Persentase Capaian'}
                ],
                'group_by': 'kategori_produk',
                'category': 'shift'
            }
        ),
        
        # 3. Foodblogger Song Fa
        ModuleConfig(
            name="Foodblogger Song Fa",
            icon="📸",
            table_name="foodblogger_sf",
            date_field="tanggal_kunjungan",
            columns=[
                date_column("tanggal_kunjungan", "Tanggal Kunjungan"),
                text_column("nama_foodblogger", "Nama Foodblogger"),
                select_column("platform", "Platform", [
                    'Instagram', 'TikTok', 'YouTube', 'Xiaohongshu', 'Blog', 'Lainnya'
                ]),
                number_column("followers", "Jumlah Followers"),
                select_column("jenis_konten", "Jenis Konten", [
                    'Food Review', 'Mukbang', 'Tutorial', 'Vlog', 'Promo'
                ]),
                number_column("biaya_entertain", "Biaya Entertain (Rp)"),
                number_column("biaya_transport", "Biaya Transport (Rp)"),
                number_column("total_biaya", "Total Biaya (Rp)"),
                textarea_column("menu_dicoba", "Menu yang Dicoba"),
                number_column("rating_makanan", "Rating Makanan (1-5)"),
                number_column("rating_service", "Rating Service (1-5)"),
                number_column("rating_kebersihan", "Rating Kebersihan (1-5)"),
                number_column("overall_rating", "Overall Rating"),
                textarea_column("feedback", "Feedback & Review"),
                text_column("link_konten", "Link Konten"),
                select_column("status", "Status", ['Draft', 'Published', 'Pending', 'Rejected']),
                text_column("pic_marketing", "PIC Marketing")
            ],
            chart_config={
                'type': ['bar', 'pie', 'scatter'],
                'metrics': [
                    {'field': 'followers', 'label': 'Followers'},
                    {'field': 'total_biaya', 'label': 'Total Biaya'},
                    {'field': 'overall_rating', 'label': 'Overall Rating'}
                ],
                'group_by': 'platform',
                'category': 'jenis_konten'
            }
        ),
        
        # 4. Condiment Song Fa
        ModuleConfig(
            name="Condiment Song Fa",
            icon="🧂",
            table_name="condiment_sf",
            date_field="tanggal",
            columns=[
                date_column("tanggal", "Tanggal"),
                text_column("nama_condiment", "Nama Condiment"),
                text_column("kode_condiment", "Kode Condiment"),
                select_column("kategori", "Kategori", [
                    'Sambal', 'Kecap', 'Bumbu Tambahan', 'Acar', 'Bawang Goreng', 'Lainnya'
                ]),
                number_column("stock_awal", "Stock Awal"),
                number_column("stock_masuk", "Stock Masuk"),
                number_column("stock_keluar", "Stock Keluar"),
                number_column("stock_akhir", "Stock Akhir"),
                number_column("minimal_stock", "Minimal Stock"),
                number_column("rata_pemakaian_harian", "Rata-rata Pemakaian Harian"),
                number_column("estimasi_habis", "Estimasi Habis (Hari)"),
                select_column("status_stock", "Status Stock", [
                    'Aman', 'Menipis', 'Kritis', 'Habis'
                ]),
                select_column("satuan", "Satuan", ['Botol', 'Sachet', 'Kg', 'Gram', 'Pcs']),
                number_column("harga_satuan", "Harga Satuan (Rp)"),
                number_column("total_nilai_stock", "Total Nilai Stock (Rp)"),
                textarea_column("keterangan", "Keterangan"),
                text_column("pic_gudang", "PIC Gudang")
            ],
            chart_config={
                'type': ['bar', 'line', 'treemap'],
                'metrics': [
                    {'field': 'stock_akhir', 'label': 'Stock Akhir'},
                    {'field': 'rata_pemakaian_harian', 'label': 'Rata-rata Pemakaian'},
                    {'field': 'estimasi_habis', 'label': 'Estimasi Habis'},
                    {'field': 'total_nilai_stock', 'label': 'Total Nilai Stock'}
                ],
                'group_by': 'kategori',
                'category': 'status_stock'
            }
        )
    ]
    
    return OutletConfig(
        name="song_fa",
        display_name="Song Fa",
        icon="🍜",
        modules=modules
    )
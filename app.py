import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
from io import BytesIO

# Import komponen manajemen konfigurasi dan database yang sudah Anda buat
from config.base_config import AppConfigManager, ModuleConfig, OutletConfig
from database import get_db

# 1. KONFIGURASI HALAMAN UTAMA
st.set_page_config(
    page_title="Sistem Manajemen Multi-Outlet Terintegrasi", 
    page_icon="🏪", 
    layout="wide"
)

# 2. INISIALISASI DATABASE & KONFIGURASI SECARA DINAMIS
db_manager = get_db()
config_manager = AppConfigManager()

# Daftarkan semua tabel ke SQLite secara otomatis dari daftar outlet yang ada
for outlet_key, outlet_cfg in config_manager.outlets.items():
    # Mengambil daftar nama tabel gabungan unik (misal: waruna_penjualan)
    for table_name in outlet_cfg.get_table_names():
        # Panggil fungsi bawaan database Anda untuk membuat tabel (ganti nama fungsi jika berbeda)
        # Jika database Anda otomatis membuat tabel saat data dimasukkan, baris ini bahkan bisa dihapus/dikomentari
        pass

# ==================== FUNGSI VISUALISASI DINAMIS ====================

def create_dynamic_chart(data, chart_config, chart_type, metric_field, group_by_field, category_field=None):
    if not data:
        return None
    
    df = pd.DataFrame(data)
    metric_label = next((m['label'] for m in chart_config.get('metrics', []) if m['field'] == metric_field), metric_field)
    
    # Aggregasi data jika kolom group_by tersedia
    if group_by_field and group_by_field in df.columns:
        agg_data = df.groupby(group_by_field)[metric_field].sum().reset_index()
        agg_data = agg_data.sort_values(metric_field, ascending=False)
    else:
        agg_data = df

    fig = None
    
    if chart_type == 'bar':
        fig = px.bar(
            agg_data, 
            x=group_by_field if group_by_field in agg_data.columns else df.index,
            y=metric_field,
            title=f'{metric_label} berdasarkan {group_by_field.replace("_", " ").title() if group_by_field else "Index"}',
            color=category_field if category_field in df.columns else None,
            color_discrete_sequence=px.colors.qualitative.Set3,
            text_auto=True
        )
    elif chart_type == 'pie':
        fig = px.pie(
            agg_data,
            values=metric_field,
            names=group_by_field if group_by_field in agg_data.columns else 'index',
            title=f'Distribusi {metric_label}',
            hole=0.3
        )
    elif chart_type == 'line':
        # Cari field tanggal secara dinamis
        date_col = next((c for c in df.columns if 'tanggal' in c or 'date' in c), None)
        if date_col:
            df[date_col] = pd.to_datetime(df[date_col])
            line_data = df.sort_values(date_col)
            fig = px.line(line_data, x=date_col, y=metric_field, title=f'Tren {metric_label}', markers=True)
        else:
            fig = px.line(agg_data, x=agg_data.columns[0], y=metric_field, title=f'Tren {metric_label}')
            
    if fig:
        fig.update_layout(template='plotly_white', height=400)
    return fig

# ==================== RENDERING FORM DINAMIS ====================

def render_dynamic_form(columns, form_key, default_values=None):
    form_data = {}
    col1, col2 = st.columns(2)
    
    for i, col in enumerate(columns):
        with col1 if i % 2 == 0 else col2:
            field_name = col['name']
            field_label = col['label']
            field_type = col['type']
            default = default_values.get(field_name, '') if default_values else col.get('default', '')
            
            if field_type == 'computed':
                st.info(f"💡 *{field_label}* dihitung otomatis sistem.")
                continue
                
            if field_type == 'text':
                form_data[field_name] = st.text_input(field_label, value=str(default), key=f"{form_key}_{field_name}")
            elif field_type == 'number':
                val = float(default) if default else 0.0
                form_data[field_name] = st.number_input(field_label, value=val, key=f"{form_key}_{field_name}")
            elif field_type == 'date':
                val = datetime.strptime(str(default)[:10], '%Y-%m-%d').date() if default else date.today()
                form_data[field_name] = st.date_input(field_label, value=val, key=f"{form_key}_{field_name}")
            elif field_type == 'select':
                options = col.get('options', [])
                idx = options.index(default) if default in options else 0
                form_data[field_name] = st.selectbox(field_label, options, index=idx, key=f"{form_key}_{field_name}")
            elif field_type == 'textarea':
                form_data[field_name] = st.text_area(field_label, value=str(default), key=f"{form_key}_{field_name}")
                
    return form_data

# ==================== CORE INTERFACE PER MODUL ====================

def render_module_interface(outlet_name, module_config):
    st.title(f"{module_config.icon} {module_config.name}")
    
    tab_dash, tab_crud, tab_export = st.tabs(["📊 Dashboard Analitik", "📋 Manajemen Data", "📤 Export"])
    table_name = module_config.table_name
    
    # Ambil data dari database berdasarkan nama outlet dan nama modul
    all_records = db_manager.get_all_records(outlet_name, table_name)
    
    # ---- 1. TAB DASHBOARD ----
    with tab_dash:
        if not all_records:
            st.info("Belum ada data untuk dianalisis. Silakan tambah data di tab Manajemen Data.")
        else:
            st.subheader("Key Performance Indicators (KPI)")
            df = pd.DataFrame(all_records)
            
            # Hitung metric jika konfigurasi bagan tersedia
            metrics = module_config.chart_config.get('metrics', [])
            if metrics:
                cols = st.columns(len(metrics))
                for idx, metric in enumerate(metrics):
                    if metric['field'] in df.columns:
                        total_val = pd.to_numeric(df[metric['field']], errors='coerce').sum()
                        with cols[idx]:
                            st.metric(label=metric['label'], value=f"{total_val:,.0f}")
            
            st.markdown("---")
            st.subheader("Grafik Analitik")
            
            if 'type' in module_config.chart_config and metrics:
                c1, c2 = st.columns(2)
                with c1:
                    selected_chart = st.selectbox("Tipe Grafik", module_config.chart_config['type'], key=f"ct_{table_name}")
                with c2:
                    selected_metric = st.selectbox("Metric Data", [m['label'] for m in metrics], key=f"mt_{table_name}")
                    metric_field = next(m['field'] for m in metrics if m['label'] == selected_metric)
                
                group_by = module_config.chart_config.get('group_by', None)
                category = module_config.chart_config.get('category', None)
                
                fig = create_dynamic_chart(all_records, module_config.chart_config, selected_chart, metric_field, group_by, category)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.caption("Konfigurasi grafik belum lengkap untuk modul ini.")

    # ---- 2. TAB CRUD (MANAJEMEN DATA) ----
    with tab_crud:
        crud_action = st.radio("Pilih Aksi", ["Lihat Data", "Tambah", "Edit", "Hapus"], horizontal=True, key=f"act_{table_name}")
        
        if crud_action == "Lihat Data":
            if all_records:
                st.dataframe(pd.DataFrame(all_records), use_container_width=True)
            else:
                st.info("Tidak ada data.")
                
        elif crud_action == "Tambah":
            with st.form(f"add_form_{table_name}"):
                input_data = render_dynamic_form(module_config.columns, f"add_{table_name}")
                submitted = st.form_submit_button("💾 Simpan Data")
                
                if submitted:
                    # Konversi object date ke String ISO untuk SQLite
                    for k, v in input_data.items():
                        if isinstance(v, (date, datetime)):
                            input_data[k] = v.isoformat()
                    
                    db_manager.add_record(outlet_name, table_name, input_data)
                    st.success("Data berhasil ditambahkan!")
                    st.rerun()
                    
        elif crud_action == "Edit":
            if not all_records:
                st.info("Tidak ada data untuk diedit.")
            else:
                options = {f"ID {r['id']}": r['id'] for r in all_records}
                selected_id = st.selectbox("Pilih ID Data untuk Diedit", list(options.keys()))
                record_to_edit = db_manager.get_record_by_id(outlet_name, table_name, options[selected_id])
                
                with st.form(f"edit_form_{table_name}"):
                    updated_data = render_dynamic_form(module_config.columns, f"edit_{table_name}", default_values=record_to_edit)
                    submitted = st.form_submit_button("✏️ Update Data")
                    
                    if submitted:
                        for k, v in updated_data.items():
                            if isinstance(v, (date, datetime)):
                                updated_data[k] = v.isoformat()
                        db_manager.update_record(outlet_name, table_name, options[selected_id], updated_data)
                        st.success("Data berhasil diperbarui!")
                        st.rerun()
                        
        elif crud_action == "Hapus":
            if not all_records:
                st.info("Tidak ada data untuk dihapus.")
            else:
                options = {f"ID {r['id']}": r['id'] for r in all_records}
                selected_id = st.selectbox("Pilih ID Data untuk Dihapus", list(options.keys()))
                confirm = st.checkbox("Saya yakin ingin menghapus data ini secara permanen")
                
                if st.button("🗑️ Hapus Data", type="primary", disabled=not confirm):
                    db_manager.delete_record(outlet_name, table_name, options[selected_id])
                    st.success("Data berhasil dihapus!")
                    st.rerun()

    # ---- 3. TAB EXPORT ----
    with tab_export:
        if all_records:
            df_export = pd.DataFrame(all_records)
            csv = df_export.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Data Berformat CSV",
                data=csv,
                file_name=f"{outlet_name}_{table_name}_{date.today()}.csv",
                mime='text/csv'
            )
        else:
            st.info("Tidak ada data untuk di-export.")

# ==================== SIDEBAR UTAMA & MULTI-OUTLET ROUTING ====================

st.sidebar.title("🏪 Control Panel Multi-Outlet")
st.sidebar.markdown("---")

# 1. Pilih Outlet Secara Dinamis dari ConfigManager
display_outlets = config_manager.get_outlet_display_names() # e.g. {'waruna': 'Waruna', 'papper_lunch': 'Papper Lunch', ...}
selected_outlet_display = st.sidebar.selectbox("📍 Pilih Outlet / Brand", list(display_outlets.values()))

# Cari key asli nama outlet berdasarkan nilai display name-nya
active_outlet_name = next(name for name, disp in display_outlets.items() if disp == selected_outlet_display)
active_config = config_manager.get_outlet(active_outlet_name)

# ==============================================================================
# GUARD CLAUSE: Memastikan active_config valid (tidak None) sebelum membaca atributnya
# Ini menghilangkan error Pylance "is not a known attribute of None"
# ==============================================================================
if active_config is None:
    st.sidebar.error("❌ Konfigurasi untuk outlet ini tidak ditemukan atau belum terdaftar.")
    st.stop() 

st.sidebar.markdown(f"### Menu {active_config.display_name}")

# 2. Ambil modul-modul yang tersedia secara eksklusif untuk outlet tersebut
module_options = [f"{mod.icon} {mod.name}" for mod in active_config.modules]
module_options.insert(0, "📊 Main Dashboard")

selected_menu_string = st.sidebar.radio("📌 Pilih Modul Kerja", module_options)

# ==================== HALAMAN KONTEN UTAMA ====================

if selected_menu_string == "📊 Main Dashboard":
    st.title(f"📊 Dashboard Utama — {active_config.display_name}")
    st.markdown(f"Selamat datang di pusat kendali operasional digital cabang **{active_config.display_name}**.")
    
    # Tampilkan statistik cepat untuk semua modul di outlet aktif
    st.subheader("Ringkasan Total Data")
    
    if active_config.modules:
        cols = st.columns(min(len(active_config.modules), 4))
        
        for idx, mod in enumerate(active_config.modules):
            total_records = len(db_manager.get_all_records(active_outlet_name, mod.table_name))
            col_idx = idx % min(len(active_config.modules), 4)
            with cols[col_idx]:
                st.metric(label=f"{mod.icon} {mod.name}", value=total_records)
    else:
        st.info("Belum ada modul kerja yang dikonfigurasi untuk cabang ini.")
            
    # Tampilkan log aktivitas terpusat untuk outlet terpilih
    st.markdown("---")
    st.subheader("🕐 Log Aktivitas Terakhir Cabang")
    logs = db_manager.get_activity_log(outlet=active_outlet_name, limit=10)
    if logs:
        for log in logs:
            st.caption(f"**[{log['timestamp']}]** {log['user']} melakukan aksi **{log['action']}** pada tabel `{log['table_name']}` (ID Record: {log['record_id']})")
    else:
        st.info("Belum ada rekam log aktivitas sistem di cabang ini.")
else:
    # Routing ke modul spesifik berdasarkan pilihan yang diklik user
    active_module = next(mod for mod in active_config.modules if f"{mod.icon} {mod.name}" == selected_menu_string)
    render_module_interface(active_outlet_name, active_module)
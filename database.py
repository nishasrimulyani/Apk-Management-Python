import sqlite3
import json
import pandas as pd # type: ignore
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple

class DatabaseManager:
    """Database manager untuk multi-outlet"""

    def __init__(self, db_path: str = "data/multi_outlet.db"):
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None
        self.cursor: Optional[sqlite3.Cursor] = None
        self._init_database()

    def _ensure_connection(self) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
        """Pastikan koneksi dan cursor tersedia"""
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
        
        if self.cursor is None:
            self.cursor = self.conn.cursor()
        
        # Type narrowing - Python tahu ini tidak None sekarang
        conn: sqlite3.Connection = self.conn
        cursor: sqlite3.Cursor = self.cursor
        
        return conn, cursor

    def get_connection(self) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
        """Get database connection"""
        return self._ensure_connection()

    def _init_database(self):
        """Initialize database dan buat tables"""
        conn, cursor = self._ensure_connection()

        # Table untuk activity log (general)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activity_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                action TEXT NOT NULL,
                table_name TEXT NOT NULL,
                record_id INTEGER,
                outlet TEXT NOT NULL,
                user TEXT DEFAULT 'System',
                old_data TEXT,
                new_data TEXT
            )
        ''')

        # Table untuk outlet
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS outlets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                display_name TEXT NOT NULL,
                description TEXT,
                is_active INTEGER DEFAULT 1,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()

        # Insert default outlets if not exists
        default_outlets = [
            ('waruna', 'Waruna', 'Outlet Waruna Utama'),
            ('papper_lunch', 'Papper Lunch', 'Outlet Papper Lunch'),
            ('song_fa', 'Song Fa', 'Outlet Song Fa')
        ]

        for name, display, desc in default_outlets:
            cursor.execute('''
                INSERT OR IGNORE INTO outlets (name, display_name, description)
                VALUES (?, ?, ?)
            ''', (name, display, desc))

        conn.commit()

    # ==================== TABLE MANAGEMENT ====================

    def create_table(self, outlet: str, table_name: str, columns: List[Dict]) -> bool:
        """Create table untuk outlet tertentu"""
        conn, cursor = self._ensure_connection()

        # Nama table: outlet_table_name
        full_table_name = f"{outlet}_{table_name}"

        # Build CREATE TABLE SQL
        col_definitions = ["id INTEGER PRIMARY KEY AUTOINCREMENT"]

        for col in columns:
            col_name = col['name']
            col_type = col.get('type', 'TEXT')

            sql_type_map = {
                'number': 'REAL',
                'date': 'TEXT',
                'time': 'TEXT',
                'boolean': 'INTEGER'
            }
            sql_type = sql_type_map.get(col_type, 'TEXT')

            col_definitions.append(f"{col_name} {sql_type}")

        # Add timestamp columns
        col_definitions.append("created_at TEXT DEFAULT CURRENT_TIMESTAMP")
        col_definitions.append("updated_at TEXT DEFAULT CURRENT_TIMESTAMP")

        sql = f"CREATE TABLE IF NOT EXISTS {full_table_name} ({', '.join(col_definitions)})"
        cursor.execute(sql)
        conn.commit()

        return True

    # ==================== CRUD OPERATIONS ====================

    def add_record(self, outlet: str, table_name: str, data: Dict) -> int:
        """Add record untuk outlet tertentu"""
        conn, cursor = self._ensure_connection()
        full_table_name = f"{outlet}_{table_name}"

        columns = list(data.keys())
        values = list(data.values())
        placeholders = ['?' for _ in columns]

        # Add timestamps
        columns.append('created_at')
        values.append(datetime.now().isoformat())
        columns.append('updated_at')
        values.append(datetime.now().isoformat())

        sql = f"INSERT INTO {full_table_name} ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"
        cursor.execute(sql, values)
        conn.commit()

        # cursor.lastrowid bisa None jika insert gagal
        record_id = cursor.lastrowid
        if record_id is None:
            raise ValueError("Failed to insert record - no row ID returned")
        
        record_id_int: int = record_id

        # Log activity
        self._log_activity('CREATE', full_table_name, record_id_int, outlet, new_data=data)

        return record_id_int

    def get_all_records(self, outlet: str, table_name: str) -> List[Dict]:
        """Get all records untuk outlet tertentu"""
        conn, cursor = self._ensure_connection()
        full_table_name = f"{outlet}_{table_name}"

        try:
            cursor.execute(f"SELECT * FROM {full_table_name} ORDER BY id DESC")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception:
            return []

    def get_record_by_id(self, outlet: str, table_name: str, record_id: int) -> Optional[Dict]:
        """Get single record by ID"""
        conn, cursor = self._ensure_connection()
        full_table_name = f"{outlet}_{table_name}"

        try:
            cursor.execute(f"SELECT * FROM {full_table_name} WHERE id = ?", (record_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        except Exception:
            return None

    def update_record(self, outlet: str, table_name: str, record_id: int, data: Dict) -> bool:
        """Update record"""
        conn, cursor = self._ensure_connection()
        full_table_name = f"{outlet}_{table_name}"

        # Get old data for logging
        old_data = self.get_record_by_id(outlet, table_name, record_id)

        # Update data
        data['updated_at'] = datetime.now().isoformat()
        set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
        values = list(data.values()) + [record_id]

        sql = f"UPDATE {full_table_name} SET {set_clause} WHERE id = ?"
        cursor.execute(sql, values)
        conn.commit()

        # Log activity
        self._log_activity('UPDATE', full_table_name, record_id, outlet, old_data=old_data, new_data=data) # type: ignore

        return True

    def delete_record(self, outlet: str, table_name: str, record_id: int) -> bool:
        """Delete record"""
        conn, cursor = self._ensure_connection()
        full_table_name = f"{outlet}_{table_name}"

        # Get old data for logging
        old_data = self.get_record_by_id(outlet, table_name, record_id)

        cursor.execute(f"DELETE FROM {full_table_name} WHERE id = ?", (record_id,))
        conn.commit()

        # Log activity
        self._log_activity('DELETE', full_table_name, record_id, outlet, old_data=old_data) # type: ignore

        return True

    # ==================== LOGGING ====================

    def _log_activity(self, action: str, table_name: str, record_id: int, outlet: str, old_data: Dict = None, new_data: Dict = None): # type: ignore
        """Log activity ke database"""
        conn, cursor = self._ensure_connection()

        old_data_str = json.dumps(old_data, default=str) if old_data else None
        new_data_str = json.dumps(new_data, default=str) if new_data else None

        cursor.execute('''
            INSERT INTO activity_log (action, table_name, record_id, outlet, user, old_data, new_data)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (action, table_name, record_id, outlet, 'System', old_data_str, new_data_str))

        conn.commit()

    def get_activity_log(self, outlet: str = None, limit: int = 100) -> List[Dict]: # type: ignore
        """Get activity log dengan filter outlet"""
        conn, cursor = self._ensure_connection()

        if outlet:
            cursor.execute('''
                SELECT * FROM activity_log
                WHERE outlet = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (outlet, limit))
        else:
            cursor.execute('''
                SELECT * FROM activity_log
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))

        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    # ==================== EXPORT FUNCTIONS ====================

    def export_to_dataframe(self, outlet: str, table_name: str) -> pd.DataFrame:
        """Export table ke pandas DataFrame"""
        conn, cursor = self._ensure_connection()
        full_table_name = f"{outlet}_{table_name}"

        try:
            df = pd.read_sql_query(f"SELECT * FROM {full_table_name} ORDER BY id DESC", conn)
            # Drop timestamp columns
            df = df.drop(columns=['created_at', 'updated_at'], errors='ignore')
            return df
        except Exception:
            return pd.DataFrame()

    def export_all_outlets(self) -> Dict[str, Dict[str, pd.DataFrame]]:
        """Export semua data dari semua outlet"""
        result = {}
        outlets = ['waruna', 'papper_lunch', 'song_fa']

        for outlet in outlets:
            outlet_data = {}

            # Get all tables for this outlet
            conn, cursor = self._ensure_connection()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE ?",
                (f"{outlet}_%",)
            )
            tables = cursor.fetchall()

            for table in tables:
                table_name = table[0].replace(f"{outlet}_", "")
                df = self.export_to_dataframe(outlet, table_name)
                if not df.empty:
                    outlet_data[table_name] = df

            if outlet_data:
                result[outlet] = outlet_data

        return result

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None


# ==================== SINGLETON INSTANCE ====================

_db_instance: Optional[DatabaseManager] = None


def get_db() -> DatabaseManager:
    """Get or create database instance (singleton)"""
    global _db_instance
    if _db_instance is None:
        _db_instance = DatabaseManager()
    return _db_instance


def init_database() -> bool:
    """Initialize database - untuk backward compatibility"""
    get_db()
    return True


# ==================== BACKWARD COMPATIBILITY FUNCTIONS ====================

def get_connection() -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    db = get_db()
    return db.get_connection()


def add_record(table_name: str, data: Dict, user: str = 'System') -> Optional[int]:
    """Parse outlet dari table_name (format: outlet_table)"""
    parts = table_name.split('_', 1)
    if len(parts) == 2:
        outlet, table = parts
        db = get_db()
        return db.add_record(outlet, table, data)
    return None


def get_all_records(table_name: str) -> List[Dict]:
    parts = table_name.split('_', 1)
    if len(parts) == 2:
        outlet, table = parts
        db = get_db()
        return db.get_all_records(outlet, table)
    return []


def get_record_by_id(table_name: str, record_id: int) -> Optional[Dict]:
    parts = table_name.split('_', 1)
    if len(parts) == 2:
        outlet, table = parts
        db = get_db()
        return db.get_record_by_id(outlet, table, record_id)
    return None


def update_record(table_name: str, record_id: int, data: Dict, user: str = 'System') -> bool:
    parts = table_name.split('_', 1)
    if len(parts) == 2:
        outlet, table = parts
        db = get_db()
        return db.update_record(outlet, table, record_id, data)
    return False


def delete_record(table_name: str, record_id: int, user: str = 'System') -> bool:
    parts = table_name.split('_', 1)
    if len(parts) == 2:
        outlet, table = parts
        db = get_db()
        return db.delete_record(outlet, table, record_id)
    return False


def get_activity_log(limit: int = 100) -> List[Dict]:
    db = get_db()
    return db.get_activity_log(limit=limit)


def export_activity_log_to_dataframe() -> pd.DataFrame:
    db = get_db()
    logs = db.get_activity_log(limit=10000)
    if logs:
        return pd.DataFrame(logs)
    return pd.DataFrame()
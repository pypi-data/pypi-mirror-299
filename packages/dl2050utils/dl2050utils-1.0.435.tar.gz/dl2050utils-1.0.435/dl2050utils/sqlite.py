import datetime
from zoneinfo import ZoneInfo
import sqlite3

# Function to adapt timezone-aware datetime to ISO-8601 string
def date_to_srt(dt):
    """Converts timezone-aware datetime to ISO-8601 string"""
    if dt is None: return None
    return dt.isoformat()

# Function to convert ISO-8601 string back to a timezone-aware datetime object
def str_to_date(s):
    if s is None: return None
    return datetime.datetime.fromisoformat(s.decode('utf-8'))

def str_to_date_2(s):
    if s is None: return None
    dt = datetime.datetime.fromisoformat(s)
    return dt.replace(tzinfo=ZoneInfo('UTC'))

def now():
    return datetime.datetime.now(ZoneInfo("UTC"))

class Sqlite():
    def __init__(self, dbname):
        dbname = dbname or ':memory:'
        # Register the adapters and converters
        sqlite3.register_adapter(datetime.datetime, date_to_srt)
        sqlite3.register_converter("DATETIME", str_to_date)
        # Create connection and ensure rows are returned as dictionaries
        self.conn = sqlite3.connect(dbname)
        self.conn.row_factory = sqlite3.Row 
    def close(self):
        self.conn.close()
    def execute(self, q, params=None):
        cursor = self.conn.cursor()
        try:
            if params:
                cursor.execute(q, params)
            else:
                cursor.execute(q)
            self.conn.commit()
        except sqlite3.DatabaseError as exc:
            print(f"Sqlite.execute error: {exc}")
            self.conn.rollback()
        return cursor
    def delete_all(self, tbl):
        self.execute(f'''DELETE FROM {tbl}''')
    def insert(self, tbl, d):
        cols,placeholders = ", ".join(d.keys()),", ".join(["?" for _ in d])
        q = f'''INSERT INTO {tbl} ({cols}) VALUES ({placeholders})'''
        values = list(d.values())
        cursor = self.execute(q, values)
        return cursor.lastrowid
    def update(self, tbl, key_col, d):
        set_clause = ", ".join([f"{col} = ?" for col in d.keys()])
        q = f"UPDATE {tbl} SET {set_clause} WHERE {key_col} = ?"
        values = list(d.values()) + [d[key_col]]
        cursor = self.execute(q, values)
        return cursor.rowcount > 0
    def delete(self, tbl, key_col, key_val):
        q = f"DELETE FROM {tbl} WHERE {key_col} = ?"
        self.execute(q, (key_val,))
    def select(self, tbl):
        cursor = self.execute(f"SELECT * FROM {tbl}")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]  # Return rows as a list of dictionaries
    def select_one(self, tbl, key_col, key_val):
        q = f"SELECT * FROM {tbl} WHERE {key_col} = ? LIMIT 1"
        cursor = self.execute(q, (key_val,))
        row = cursor.fetchone()
        return dict(row) if row else None
    def select_and_update(self, tbl, key_col, key_val, d):
            d1 = self.select_one(tbl, key_col, key_val)
            d = {**d1, **d}
            return self.update(tbl, key_col, d)

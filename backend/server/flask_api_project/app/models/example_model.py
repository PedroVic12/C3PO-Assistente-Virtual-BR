import sqlite3
from pathlib import Path

class ExampleModel:
    def __init__(self):
        self.db_path = "database.db"
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS examples (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def find_all(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM examples")
        rows = cursor.fetchall()
        conn.close()
        
        # Converter para lista de dicionários
        columns = ['id', 'name', 'description', 'created_at', 'updated_at']
        return [dict(zip(columns, row)) for row in rows]

    def find_by_id(self, id):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM examples WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            columns = ['id', 'name', 'description', 'created_at', 'updated_at']
            return dict(zip(columns, row))
        return None

    def create(self, data):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO examples (name, description) VALUES (?, ?)",
            (data.get('name'), data.get('description'))
        )
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return new_id

    def update(self, id, data):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE examples SET name = ?, description = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (data.get('name'), data.get('description'), id)
        )
        affected = cursor.rowcount
        conn.commit()
        conn.close()
        return affected > 0

    def delete(self, id):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM examples WHERE id = ?", (id,))
        affected = cursor.rowcount
        conn.commit()
        conn.close()
        return affected > 0

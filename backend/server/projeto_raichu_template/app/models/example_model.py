import sqlite3

DB = "database.db"

class ExampleModel:
    def __init__(self):
        self.db_path = DB
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
        cols = ['id','name','description','created_at','updated_at']
        return [dict(zip(cols, r)) for r in rows]

    def create(self, data):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO examples (name, description) VALUES (?, ?)",
                       (data.get('name'), data.get('description')))
        conn.commit()
        nid = cursor.lastrowid
        conn.close()
        return nid

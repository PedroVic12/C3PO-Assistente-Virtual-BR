#!/usr/bin/env python3
# cli.py - cria controllers e models em app/controllers e app/models
import argparse
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def create_controller(name: str):
    cname = name.lower()
    path = ROOT / "app" / "controllers" / f"{cname}_controller.py"
    if path.exists():
        print("Controller já existe:", path)
        return
    content = f'''from flask import jsonify
from app.models.{cname}_model import {name.capitalize()}Model

class {name.capitalize()}Controller:
    def __init__(self):
        self.model = {name.capitalize()}Model()

    def get_all(self):
        try:
            data = self.model.find_all()
            return jsonify({{"success": True, "data": data, "count": len(data)}})
        except Exception as e:
            return jsonify({{"success": False, "error": str(e)}}), 500

    def get_by_id(self, id):
        try:
            item = self.model.find_by_id(id)
            if item:
                return jsonify({{"success": True, "data": item}})
            return jsonify({{"success": False, "error": "Item não encontrado"}}), 404
        except Exception as e:
            return jsonify({{"success": False, "error": str(e)}}), 500

    def create(self, data):
        try:
            new_id = self.model.create(data)
            return jsonify({{"success": True, "id": new_id}}), 201
        except Exception as e:
            return jsonify({{"success": False, "error": str(e)}}), 500
'''
    path.write_text(content)
    print("Controller criado:", path)

def create_model(name: str):
    cname = name.lower()
    path = ROOT / "app" / "models" / f"{cname}_model.py"
    if path.exists():
        print("Model já existe:", path)
        return
    content = f'''import sqlite3
from pathlib import Path

DB = "database.db"

class {name.capitalize()}Model:
    def __init__(self):
        self.db_path = DB
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS {cname}s (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    def find_all(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {cname}s")
        rows = cursor.fetchall()
        conn.close()
        cols = ['id','name','description','created_at','updated_at']
        return [dict(zip(cols, r)) for r in rows]

    def find_by_id(self, id):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {cname}s WHERE id = ?", (id,))
        r = cursor.fetchone()
        conn.close()
        if r:
            cols = ['id','name','description','created_at','updated_at']
            return dict(zip(cols, r))
        return None

    def create(self, data):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO {cname}s (name, description) VALUES (?, ?)",
                       (data.get('name'), data.get('description')))
        conn.commit()
        nid = cursor.lastrowid
        conn.close()
        return nid
'''
    path.write_text(content)
    print("Model criado:", path)

def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd")
    c1 = sub.add_parser("create-controller"); c1.add_argument("name")
    c2 = sub.add_parser("create-model"); c2.add_argument("name")
    args = p.parse_args()
    if args.cmd == "create-controller":
        create_controller(args.name)
    elif args.cmd == "create-model":
        create_model(args.name)
    else:
        p.print_help()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import argparse
import os
import sys
from pathlib import Path

def create_controller(name):
    """Cria um novo controller"""
    controller_name = f"{name.lower()}_controller.py"
    controller_path = f"app/controllers/{controller_name}"
    
    if os.path.exists(controller_path):
        print(f"Controller {controller_name} já existe!")
        return False
    
    content = f'''from flask import jsonify
from app.models.{name.lower()}_model import {name.capitalize()}Model

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
            # Validar dados aqui
            new_id = self.model.create(data)
            return jsonify({{"success": True, "id": new_id, "message": "Item criado com sucesso"}}), 201
        except Exception as e:
            return jsonify({{"success": False, "error": str(e)}}), 500

    def update(self, id, data):
        try:
            updated = self.model.update(id, data)
            if updated:
                return jsonify({{"success": True, "message": "Item atualizado com sucesso"}})
            return jsonify({{"success": False, "error": "Item não encontrado"}}), 404
        except Exception as e:
            return jsonify({{"success": False, "error": str(e)}}), 500

    def delete(self, id):
        try:
            deleted = self.model.delete(id)
            if deleted:
                return jsonify({{"success": True, "message": "Item deletado com sucesso"}})
            return jsonify({{"success": False, "error": "Item não encontrado"}}), 404
        except Exception as e:
            return jsonify({{"success": False, "error": str(e)}}), 500
'''
    
    with open(controller_path, 'w') as f:
        f.write(content)
    
    print(f"Controller criado: {controller_path}")
    return True

def create_model(name):
    """Cria um novo model"""
    model_name = f"{name.lower()}_model.py"
    model_path = f"app/models/{model_name}"
    
    if os.path.exists(model_path):
        print(f"Model {model_name} já existe!")
        return False
    
    content = f'''import sqlite3
from pathlib import Path

class {name.capitalize()}Model:
    def __init__(self):
        self.db_path = "database.db"
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
CREATE TABLE IF NOT EXISTS {name.lower()}s (
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
        cursor.execute(f"SELECT * FROM {name.lower()}s")
        rows = cursor.fetchall()
        conn.close()
        
        # Converter para lista de dicionários
        columns = ['id', 'name', 'description', 'created_at', 'updated_at']
        return [dict(zip(columns, row)) for row in rows]

    def find_by_id(self, id):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {name.lower()}s WHERE id = ?", (id,))
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
            f"INSERT INTO {name.lower()}s (name, description) VALUES (?, ?)",
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
            f"UPDATE {name.lower()}s SET name = ?, description = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (data.get('name'), data.get('description'), id)
        )
        affected = cursor.rowcount
        conn.commit()
        conn.close()
        return affected > 0

    def delete(self, id):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {name.lower()}s WHERE id = ?", (id,))
        affected = cursor.rowcount
        conn.commit()
        conn.close()
        return affected > 0
'''
    
    with open(model_path, 'w') as f:
        f.write(content)
    
    print(f"Model criado: {model_path}")
    return True

def main():
    parser = argparse.ArgumentParser(description="CLI para gerenciar projeto Flask")
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponíveis')

    # Comando para criar controller
    parser_controller = subparsers.add_parser('create-controller', help='Criar um novo controller')
    parser_controller.add_argument('name', help='Nome do controller (ex: user, product)')

    # Comando para criar model
    parser_model = subparsers.add_parser('create-model', help='Criar um novo model')
    parser_model.add_argument('name', help='Nome do model (ex: user, product)')

    args = parser.parse_args()

    if args.command == 'create-controller':
        create_controller(args.name)
    elif args.command == 'create-model':
        create_model(args.name)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()

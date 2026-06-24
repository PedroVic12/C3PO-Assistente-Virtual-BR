import argparse
import sqlite3
import os

DB_FILE = 'backend/cli.db'

def setup_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS generated_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_type TEXT NOT NULL,
            name TEXT NOT NULL,
            path TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def create_model(name):
    path = f'backend/models/{name.lower()}.py'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(f'# Model: {name.capitalize()}\n\n')
        f.write(f'class {name.capitalize()}:\n')
        f.write(f'    def __init__(self):\n')
        f.write(f'        pass\n')
    record_file('model', name, path)
    print(f"✅ Model '{name}' criado em '{path}'")

def create_controller(name):
    path = f'backend/controllers/{name.lower()}_controller.py'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(f'# Controller: {name.capitalize()}Controller\n\n')
        f.write(f'class {name.capitalize()}Controller:\n')
        f.write(f'    def __init__(self):\n')
        f.write(f'        pass\n')
    record_file('controller', name, path)
    print(f"✅ Controller '{name}' criado em '{path}'")

def record_file(file_type, name, path):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO generated_files (file_type, name, path) VALUES (?, ?, ?)",
                   (file_type, name, path))
    conn.commit()
    conn.close()

def main():
    parser = argparse.ArgumentParser(description='CLI para gerar arquivos de template.')
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Comando 'create'
    parser_create = subparsers.add_parser('create', help='Cria um novo arquivo.')
    create_subparsers = parser_create.add_subparsers(dest='type', required=True)

    # Subcomando 'create model'
    parser_model = create_subparsers.add_parser('model', help='Cria um novo model.')
    parser_model.add_argument('name', type=str, help='Nome do model.')

    # Subcomando 'create controller'
    parser_controller = create_subparsers.add_parser('controller', help='Cria um novo controller.')
    parser_controller.add_argument('name', type=str, help='Nome do controller.')

    args = parser.parse_args()
    
    setup_database()

    if args.command == 'create':
        if args.type == 'model':
            create_model(args.name)
        elif args.type == 'controller':
            create_controller(args.name)

if __name__ == '__main__':
    main()

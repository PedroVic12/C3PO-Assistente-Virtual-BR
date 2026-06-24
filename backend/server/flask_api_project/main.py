from flask import Flask, request, jsonify, render_template
from app.controllers.example_controller import ExampleController
from app.models.example_model import ExampleModel
from app.controllers.product_controller import ProductController
from app.models.product_model import ProductModel
import os
from pathlib import Path

app = Flask(__name__)

# Configurar caminho absoluto para templates
BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "app" / "templates"
app.template_folder = str(TEMPLATES_DIR)

PORTA = 5555
db = ExampleModel()
print("Banco de dados SQlite = ", db)
query = db.find_all()
print(query)

# Configurações
app.config['SECRET_KEY'] = 'sua-chave-secreta-aqui'

# Inicializar controladores
example_controller = ExampleController()
product_controller = ProductController()

#! Router
@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/api/examples', methods=['GET'])
def get_examples():
    """API: Buscar todos os exemplos"""
    return example_controller.get_all()

@app.route('/api/examples/<int:id>', methods=['GET'])
def get_example(id):
    """API: Buscar exemplo por ID"""
    return example_controller.get_by_id(id)

@app.route('/api/examples', methods=['POST'])
def create_example():
    """API: Criar novo exemplo"""
    data = request.get_json()
    return example_controller.create(data)

@app.route('/api/examples/<int:id>', methods=['PUT'])
def update_example(id):
    """API: Atualizar exemplo"""
    data = request.get_json()
    return example_controller.update(id, data)

@app.route('/api/examples/<int:id>', methods=['DELETE'])
def delete_example(id):
    """API: Deletar exemplo"""
    return example_controller.delete(id)

@app.route('/api/products', methods=['GET'])
def get_products():
    """API: Buscar todos os produtos"""
    return product_controller.get_all()

@app.route('/api/products/<int:id>', methods=['GET'])
def get_product(id):
    """API: Buscar produto por ID"""
    return product_controller.get_by_id(id)

@app.route('/api/products', methods=['POST'])
def create_product():
    """API: Criar novo produto"""
    data = request.get_json()
    return product_controller.create(data)

@app.route('/api/products/<int:id>', methods=['PUT'])
def update_product(id):
    """API: Atualizar produto"""
    data = request.get_json()
    return product_controller.update(id, data)

@app.route('/api/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    """API: Deletar produto"""
    return product_controller.delete(id)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint de health check"""
    return jsonify({"status": "healthy", "message": "API está funcionando"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=PORTA)

import os
from flask import Flask, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy

# --- CONFIGURAÇÃO DA APLICAÇÃO FLASK ---

# Cria a instância da aplicação Flask
app = Flask(__name__, template_folder='.', static_folder='.')

# Define o caminho base do projeto
basedir = os.path.abspath(os.path.dirname(__file__))

# Configura o URI do banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'raichu.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa a extensão SQLAlchemy
db = SQLAlchemy(app)


# --- MODELOS DO BANCO DE DADOS (EXEMPLO) ---

# Embora o frontend use localStorage, esta estrutura está pronta para integração.
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Task {self.id}: {self.text}>'

# --- ROTAS DA APLICAÇÃO ---

@app.route('/')
def index():
    """
    Rota principal que renderiza a interface do usuário.
    """
    return render_template('frontend.html')

@app.route('/favicon.ico')
def favicon():
    """
    Serve o favicon para evitar erros 404 no log.
    """
    # Este é um exemplo simples, idealmente você teria um arquivo favicon.ico na sua pasta
    return '', 204


# --- EXECUÇÃO DA APLICAÇÃO ---

if __name__ == '__main__':
    # Cria as tabelas do banco de dados se não existirem
    with app.app_context():
        db.create_all()
    
    # Inicia o servidor web Flask
    # O modo de depuração (debug=True) é útil para desenvolvimento.
    app.run(debug=True)


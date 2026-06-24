from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Database Configuration
db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'pikachu_database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Task/Client log model
class TaskLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250))
    status = db.Column(db.String(20), default='Pending')

with app.app_context():
    db.create_all()

@app.route('/')
def health_check():
    return jsonify({
        "status": "ONLINE",
        "service": "Pikachu API Rest Server",
        "database": "SQLite Initialized"
    })

@app.route('/api/tasks', methods=['GET', 'POST'])
def handle_tasks():
    if request.method == 'POST':
        data = request.json
        new_task = TaskLog(
            title=data.get('title'),
            description=data.get('description'),
            status=data.get('status', 'Pending')
        )
        db.session.add(new_task)
        db.session.commit()
        return jsonify({"message": "Tarefa criada!", "id": new_task.id}), 201
    
    tasks = TaskLog.query.all()
    return jsonify([{
        "id": t.id,
        "title": t.title,
        "description": t.description,
        "status": t.status
    } for t in tasks])

if __name__ == '__main__':
    app.run(port=5555, debug=True)

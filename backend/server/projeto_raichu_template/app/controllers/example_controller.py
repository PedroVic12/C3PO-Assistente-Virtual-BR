from flask import jsonify
from app.models.example_model import ExampleModel

class ExampleController:
    def __init__(self):
        self.model = ExampleModel()

    def get_all(self):
        try:
            data = self.model.find_all()
            return jsonify({"success": True, "data": data, "count": len(data)})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    def create(self, data):
        try:
            nid = self.model.create(data)
            return jsonify({"success": True, "id": nid}), 201
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

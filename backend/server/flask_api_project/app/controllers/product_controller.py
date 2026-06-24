from flask import jsonify
from app.models.product_model import ProductModel

class ProductController:
    def __init__(self):
        self.model = ProductModel()

    def get_all(self):
        try:
            data = self.model.find_all()
            return jsonify({"success": True, "data": data, "count": len(data)})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    def get_by_id(self, id):
        try:
            item = self.model.find_by_id(id)
            if item:
                return jsonify({"success": True, "data": item})
            return jsonify({"success": False, "error": "Item não encontrado"}), 404
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    def create(self, data):
        try:
            # Validar dados aqui
            new_id = self.model.create(data)
            return jsonify({"success": True, "id": new_id, "message": "Item criado com sucesso"}), 201
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    def update(self, id, data):
        try:
            updated = self.model.update(id, data)
            if updated:
                return jsonify({"success": True, "message": "Item atualizado com sucesso"})
            return jsonify({"success": False, "error": "Item não encontrado"}), 404
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    def delete(self, id):
        try:
            deleted = self.model.delete(id)
            if deleted:
                return jsonify({"success": True, "message": "Item deletado com sucesso"})
            return jsonify({"success": False, "error": "Item não encontrado"}), 404
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

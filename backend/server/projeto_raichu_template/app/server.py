# app/server.py
from flask import Flask, render_template, jsonify, request, send_from_directory
from pathlib import Path
import os

class RaichuWebServer:
    def __init__(self):
        project_root = Path(__file__).resolve().parent.parent
        templates_dir = str(project_root / "app" / "templates")
        static_dir = str(project_root / "app" / "static")

        os.makedirs(templates_dir, exist_ok=True)
        os.makedirs(static_dir, exist_ok=True)

        self.app = Flask(
            __name__,
            template_folder=templates_dir,
            static_folder=static_dir,
            static_url_path="/static"
        )

        # Import controllers lazily to avoid circular imports in generation
        try:
            from app.controllers.example_controller import ExampleController
            self.example_controller = ExampleController()
        except Exception:
            self.example_controller = None

        @self.app.route("/")
        def index():
            return render_template("index.html")

        # API endpoints (exemplo)
        @self.app.route("/api/examples", methods=["GET"])
        def api_get_examples():
            if self.example_controller:
                return self.example_controller.get_all()
            return jsonify({"success": False, "error": "Controller não disponível"}), 500

        @self.app.route("/api/examples", methods=["POST"])
        def api_create_example():
            data = request.get_json() or {}
            if self.example_controller:
                return self.example_controller.create(data)
            return jsonify({"success": False, "error": "Controller não disponível"}), 500

        @self.app.route("/api/health", methods=["GET"])
        def health():
            return jsonify({"status": "healthy", "message": "API rodando"})

        # Serve build do Astro se existir em frontend/dist
        @self.app.route("/site/<path:filename>")
        def site_static(filename):
            site_build = project_root / "frontend" / "dist"
            if (site_build / filename).exists():
                return send_from_directory(str(site_build), filename)
            return ("Arquivo não encontrado", 404)

    def run(self, host="0.0.0.0", port=5000, debug=True):
        print(f"⚡ RaichuWebServer rodando em http://{host}:{port}")
        self.app.run(host=host, port=port, debug=debug)

#!/usr/bin/env python3
"""
ONS PLC PVRV - Ecossistema Flask MVC com Pipeline de Dados
Autor: Pedro Victor
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import sqlite3
import pandas as pd
import json
import os
from datetime import datetime
import logging
from typing import Dict, List, Any, Optional
import PyPDF2
import openpyxl
from abc import ABC, abstractmethod
from Scripts.notifications import notification_manager
import markdown as md
from flask import render_template_string
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Obter o diretório do arquivo atual para localizar templates
FOLDER_PROJECT = "flask-backend-project"
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), FOLDER_PROJECT)
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")
DATA_DIR = os.path.join(BASE_DIR, "data")

app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)
CORS(app)
app.config["SECRET_KEY"] = "ons-pvrv-secret-key"

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


class BaseModel(ABC):
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = os.path.join(DATA_DIR, "database.db")
        self.db_path = db_path
        self.ensure_database()

    @abstractmethod
    def create_table(self):
        pass

    def ensure_database(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.create_table()


class TaskModel(BaseModel):
    def create_table(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    status TEXT DEFAULT 'pending',
                    priority INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

    def get_all(self) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM tasks ORDER BY created_at DESC")
            return [dict(row) for row in cursor.fetchall()]

    def get_by_id(self, task_id: int) -> Optional[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def create(self, data: Dict) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                INSERT INTO tasks (title, description, status, priority)
                VALUES (?, ?, ?, ?)
            """,
                (
                    data["title"],
                    data.get("description", ""),
                    data.get("status", "pending"),
                    data.get("priority", 1),
                ),
            )
            return cursor.lastrowid

    def update(self, task_id: int, data: Dict) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                UPDATE tasks
                SET title = ?, description = ?, status = ?, priority = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """,
                (
                    data["title"],
                    data.get("description", ""),
                    data.get("status", "pending"),
                    data.get("priority", 1),
                    task_id,
                ),
            )
            return cursor.rowcount > 0

    def delete(self, task_id: int) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            return cursor.rowcount > 0


class DataFileModel(BaseModel):
    def create_table(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS data_files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    file_type TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT
                )
            """
            )

    def register_file(
        self, filename: str, file_type: str, file_path: str, metadata: Dict = None
    ):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                INSERT INTO data_files (filename, file_type, file_path, metadata)
                VALUES (?, ?, ?, ?)
            """,
                (filename, file_type, file_path, json.dumps(metadata or {})),
            )
            return cursor.lastrowid

    def get_all(self) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM data_files ORDER BY processed_at DESC")
            return [dict(row) for row in cursor.fetchall()]


class BaseController:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)


class TaskController(BaseController):
    def __init__(self):
        super().__init__()
        self.model = TaskModel()

    def get_all_tasks(self) -> List[Dict]:
        return self.model.get_all()

    def get_task(self, task_id: int) -> Optional[Dict]:
        return self.model.get_by_id(task_id)

    def create_task(self, data: Dict) -> Dict:
        try:
            task_id = self.model.create(data)
            task_title = data.get("title", "Sem título")
            # 🔔 Notificar com TTS
            notification_manager.notify_task_created(task_title, task_id)
            return {
                "success": True,
                "id": task_id,
                "message": "Tarefa criada com sucesso",
            }
        except Exception as e:
            self.logger.error(f"Erro ao criar tarefa: {e}")
            notification_manager.notify_error("Erro ao Criar Tarefa", str(e))
            return {"success": False, "error": str(e)}

    def update_task(self, task_id: int, data: Dict) -> Dict:
        try:
            success = self.model.update(task_id, data)
            if success:
                task_title = data.get("title", "Sem título")
                # 🔔 Notificar com TTS
                notification_manager.notify_task_updated(task_title)
                return {"success": True, "message": "Tarefa atualizada com sucesso"}
            return {"success": False, "error": "Tarefa não encontrada"}
        except Exception as e:
            self.logger.error(f"Erro ao atualizar tarefa: {e}")
            notification_manager.notify_error("Erro ao Atualizar Tarefa", str(e))
            return {"success": False, "error": str(e)}

    def delete_task(self, task_id: int) -> Dict:
        try:
            # Buscar o título antes de deletar
            task = self.model.get_by_id(task_id)
            success = self.model.delete(task_id)
            if success:
                task_title = task.get("title", "Sem título") if task else "Tarefa"
                # 🔔 Notificar com TTS
                notification_manager.notify_task_deleted(task_title)
                return {"success": True, "message": "Tarefa deletada com sucesso"}
            return {"success": False, "error": "Tarefa não encontrada"}
        except Exception as e:
            self.logger.error(f"Erro ao deletar tarefa: {e}")
            notification_manager.notify_error("Erro ao Deletar Tarefa", str(e))
            return {"success": False, "error": str(e)}


class PandaController(BaseController):
    def __init__(self):
        super().__init__()
        self.data_model = DataFileModel()
        self.upload_dir = os.path.join(BASE_DIR, "data", "uploads")
        self.export_dir = os.path.join(BASE_DIR, "data", "exports")
        os.makedirs(self.upload_dir, exist_ok=True)
        os.makedirs(self.export_dir, exist_ok=True)

    def process_xlsx(self, file_path: str) -> Dict:
        try:
            df = pd.read_excel(file_path)
            analysis = {
                "rows": len(df),
                "columns": len(df.columns),
                "column_names": df.columns.tolist(),
                "data_types": {str(k): str(v) for k, v in df.dtypes.to_dict().items()},
                "sample_data": df.head().to_dict("records"),
            }
            filename = os.path.basename(file_path)
            self.data_model.register_file(
                filename=filename,
                file_type="xlsx",
                file_path=file_path,
                metadata=analysis,
            )
            # 🔔 Notificar com TTS
            notification_manager.notify_file_processed(filename, "Excel")
            return {"success": True, "analysis": analysis}
        except Exception as e:
            self.logger.error(f"Erro ao processar XLSX: {e}")
            notification_manager.notify_error("Erro ao Processar Excel", str(e))
            return {"success": False, "error": str(e)}

    def process_txt(self, file_path: str) -> Dict:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            analysis = {
                "lines": len(content.splitlines()),
                "characters": len(content),
                "words": len(content.split()),
                "preview": content[:500] + "..." if len(content) > 500 else content,
            }
            self.data_model.register_file(
                filename=os.path.basename(file_path),
                file_type="txt",
                file_path=file_path,
                metadata=analysis,
            )
            return {"success": True, "analysis": analysis}
        except Exception as e:
            self.logger.error(f"Erro ao processar TXT: {e}")
            return {"success": False, "error": str(e)}

    def process_pdf(self, file_path: str) -> Dict:
        try:
            with open(file_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""
            analysis = {
                "pages": len(reader.pages),
                "characters": len(text),
                "words": len(text.split()),
                "preview": text[:500] + "..." if len(text) > 500 else text,
            }
            filename = os.path.basename(file_path)
            self.data_model.register_file(
                filename=filename,
                file_type="pdf",
                file_path=file_path,
                metadata=analysis,
            )
            # 🔔 Notificar com TTS
            notification_manager.notify_file_processed(filename, "PDF")
            return {"success": True, "analysis": analysis}
        except Exception as e:
            self.logger.error(f"Erro ao processar PDF: {e}")
            notification_manager.notify_error("Erro ao Processar PDF", str(e))
            return {"success": False, "error": str(e)}

    def export_to_xlsx(self, data: List[Dict], filename: str = None) -> str:
        if not filename:
            filename = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        file_path = os.path.join(self.export_dir, filename)
        df = pd.DataFrame(data)
        df.to_excel(file_path, index=False)
        return file_path

    def import_tasks_from_xlsx(self, file_path: str) -> Dict:
        """Importa tarefas de um arquivo xlsx. Procura colunas 'title'/'titulo' e 'description'/'descricao'."""
        try:
            df = pd.read_excel(file_path)
            created = []
            model = TaskModel(self.data_model.db_path)
            for _, row in df.iterrows():
                # tentar várias variações de nomes de coluna
                title = None
                for key in ("title", "titulo", "Título", "titulo", "nome"):
                    if key in df.columns:
                        title = str(row.get(key)) if pd.notna(row.get(key)) else None
                        if title:
                            break
                if not title:
                    # pular linha sem título
                    continue
                description = None
                for key in ("description", "descricao", "descrição", "notes"):
                    if key in df.columns:
                        description = (
                            str(row.get(key)) if pd.notna(row.get(key)) else ""
                        )
                        break
                data = {"title": title, "description": description or ""}
                tid = model.create(data)
                created.append({"id": tid, "title": title})
            return {"success": True, "created": created, "count": len(created)}
        except Exception as e:
            self.logger.error(f"Erro ao importar tarefas XLSX: {e}")
            return {"success": False, "error": str(e)}

    def process_md(self, file_path: str) -> Dict:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            analysis = {
                "lines": len(content.splitlines()),
                "characters": len(content),
                "words": len(content.split()),
                "preview": content[:1000] + "..." if len(content) > 1000 else content,
            }
            filename = os.path.basename(file_path)
            self.data_model.register_file(
                filename=filename,
                file_type="md",
                file_path=file_path,
                metadata=analysis,
            )
            notification_manager.notify_file_processed(filename, "Markdown")
            return {"success": True, "analysis": analysis}
        except Exception as e:
            self.logger.error(f"Erro ao processar MD: {e}")
            notification_manager.notify_error("Erro ao Processar Markdown", str(e))
            return {"success": False, "error": str(e)}

    def export_to_md(self, data: List[Dict], filename: str = None) -> str:
        if not filename:
            filename = f"tasks_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        file_path = os.path.join(self.export_dir, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"# Export de Tarefas - {datetime.now().isoformat()}\n\n")
            for t in data:
                f.write(f"- **{t.get('title','Sem título')}** (id: {t.get('id')})\n")
                if t.get("description"):
                    f.write(f"  - {t.get('description')}\n")
        return file_path

    def export_to_pdf(self, data: List[Dict], filename: str = None) -> str:
        if not filename:
            filename = f"tasks_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        file_path = os.path.join(self.export_dir, filename)
        c = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter
        y = height - 50
        c.setFont("Helvetica-Bold", 14)
        c.drawString(40, y, "Export de Tarefas")
        y -= 30
        c.setFont("Helvetica", 10)
        for t in data:
            line = f"- {t.get('title','Sem título')} (id: {t.get('id')})"
            c.drawString(40, y, line)
            y -= 14
            if t.get("description"):
                desc = t.get("description")
                # wrap simple long descriptions
                for i in range(0, len(desc), 80):
                    c.drawString(60, y, desc[i : i + 80])
                    y -= 12
            y -= 6
            if y < 80:
                c.showPage()
                y = height - 50
                c.setFont("Helvetica", 10)
        c.save()
        return file_path

    def get_processed_files(self) -> List[Dict]:
        return self.data_model.get_all()


task_controller = TaskController()
panda_controller = PandaController()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/tasks", methods=["GET"])
def api_get_tasks():
    return jsonify(task_controller.get_all_tasks())


@app.route("/api/tasks", methods=["POST"])
def api_create_task():
    data = request.get_json()
    result = task_controller.create_task(data)
    return jsonify(result)


@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def api_update_task(task_id):
    data = request.get_json()
    result = task_controller.update_task(task_id, data)
    return jsonify(result)


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def api_delete_task(task_id):
    result = task_controller.delete_task(task_id)
    return jsonify(result)


@app.route("/api/upload", methods=["POST"])
def api_upload_file():
    if "file" not in request.files:
        return jsonify({"success": False, "error": "Nenhum arquivo enviado"})
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"success": False, "error": "Nenhum arquivo selecionado"})
    filename = file.filename
    file_path = os.path.join(panda_controller.upload_dir, filename)
    file.save(file_path)
    file_ext = filename.lower().split(".")[-1]
    if file_ext == "xlsx":
        result = panda_controller.process_xlsx(file_path)
    elif file_ext == "txt":
        result = panda_controller.process_txt(file_path)
    elif file_ext == "pdf":
        result = panda_controller.process_pdf(file_path)
    elif file_ext == "md" or file_ext == "markdown":
        result = panda_controller.process_md(file_path)
    else:
        result = {
            "success": False,
            "error": f"Tipo de arquivo não suportado: {file_ext}",
        }
    return jsonify(result)


@app.route("/api/import/tasks", methods=["POST"])
def api_import_tasks():
    if "file" not in request.files:
        return jsonify({"success": False, "error": "Nenhum arquivo enviado"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"success": False, "error": "Nenhum arquivo selecionado"}), 400
    filename = file.filename
    file_path = os.path.join(panda_controller.upload_dir, filename)
    file.save(file_path)
    file_ext = filename.lower().split(".")[-1]
    if file_ext in ("xlsx", "xls"):
        result = panda_controller.import_tasks_from_xlsx(file_path)
        return jsonify(result)
    return (
        jsonify(
            {
                "success": False,
                "error": "Tipo de arquivo não suportado para import: somente xlsx/xls",
            }
        ),
        400,
    )


@app.route("/api/export/tasks")
def api_export_tasks():
    tasks = task_controller.get_all_tasks()
    file_path = panda_controller.export_to_xlsx(tasks, "tasks_export.xlsx")
    return send_file(file_path, as_attachment=True)


@app.route("/api/export/tasks.md")
def api_export_tasks_md():
    tasks = task_controller.get_all_tasks()
    file_path = panda_controller.export_to_md(tasks, "tasks_export.md")
    return send_file(file_path, as_attachment=True)


@app.route("/api/export/tasks.pdf")
def api_export_tasks_pdf():
    tasks = task_controller.get_all_tasks()
    file_path = panda_controller.export_to_pdf(tasks, "tasks_export.pdf")
    return send_file(file_path, as_attachment=True)


@app.route("/files/view/<int:file_id>")
def view_file(file_id: int):
    files = panda_controller.get_processed_files()
    file_entry = next((f for f in files if f.get("id") == file_id), None)
    if not file_entry:
        return jsonify({"success": False, "error": "Arquivo não encontrado"}), 404
    file_path = file_entry.get("file_path")
    ftype = file_entry.get("file_type")
    if ftype == "pdf":
        return send_file(file_path, as_attachment=False, mimetype="application/pdf")
    if ftype == "md":
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            html = md.markdown(content, extensions=["fenced_code", "tables"])
            template = """
            <!doctype html>
            <html lang=\"pt-BR\"> <head> <meta charset=\"utf-8\"> <meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"> <title>Visualização Markdown</title>
            <style>body{font-family:Arial,Helvetica,sans-serif;padding:20px;max-width:900px;margin:auto;} pre{background:#2d2d2d;color:#f8f8f2;padding:10px;border-radius:6px;overflow:auto;} code{background:#f5f5f5;padding:2px 4px;border-radius:4px;}</style>
            </head><body>{{content|safe}}</body></html>
            """
            return render_template_string(template, content=html)
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    # fallback: send raw file
    return send_file(file_path, as_attachment=False)


@app.route("/api/processed-files", methods=["GET"])
def api_get_processed_files():
    files = panda_controller.get_processed_files()
    return jsonify(files)


@app.route("/api/sync", methods=["POST"])
def api_sync_data():
    return jsonify({"success": True, "message": "Dados sincronizados com sucesso"})


@app.route("/api/status")
def api_status():
    return jsonify(
        {
            "status": "online",
            "timestamp": datetime.now().isoformat(),
            "tasks_count": len(task_controller.get_all_tasks()),
            "files_count": len(panda_controller.get_processed_files()),
        }
    )


@app.route("/api/console", methods=["POST"])
def api_console():
    data = request.get_json() or {}
    cmd = (data.get("command") or "").strip()
    if not cmd:
        return jsonify({"success": False, "output": "Nenhum comando fornecido"}), 400

    # comandos simples suportados
    try:
        if cmd.lower() in ("list tasks", "listar tarefas"):
            tasks = task_controller.get_all_tasks()
            return jsonify({"success": True, "output": tasks})

        if cmd.lower().startswith("create task ") or cmd.lower().startswith(
            "criar tarefa "
        ):
            # formato: create task Título|Descrição
            payload = cmd.split(" ", 2)[2]
            parts = payload.split("|", 1)
            title = parts[0].strip()
            description = parts[1].strip() if len(parts) > 1 else ""
            result = task_controller.create_task(
                {"title": title, "description": description}
            )
            return jsonify({"success": True, "output": result})

        if cmd.lower() in ("export excel", "export xlsx", "exportar excel"):
            path = panda_controller.export_to_xlsx(task_controller.get_all_tasks())
            return jsonify(
                {"success": True, "output": {"path": path, "url": "/api/export/tasks"}}
            )

        if cmd.lower() in ("export md", "export markdown", "exportar md"):
            path = panda_controller.export_to_md(task_controller.get_all_tasks())
            return jsonify(
                {
                    "success": True,
                    "output": {"path": path, "url": "/api/export/tasks.md"},
                }
            )

        if cmd.lower() in ("export pdf", "exportar pdf"):
            path = panda_controller.export_to_pdf(task_controller.get_all_tasks())
            return jsonify(
                {
                    "success": True,
                    "output": {"path": path, "url": "/api/export/tasks.pdf"},
                }
            )

        if cmd.lower() in ("list files", "listar arquivos"):
            files = panda_controller.get_processed_files()
            return jsonify({"success": True, "output": files})

        if cmd.lower().startswith("view file ") or cmd.lower().startswith(
            "ver arquivo "
        ):
            parts = cmd.split()
            try:
                fid = int(parts[-1])
                url = f"/files/view/{fid}"
                return jsonify({"success": True, "output": {"url": url}})
            except Exception:
                return jsonify({"success": False, "output": "ID inválido"}), 400

        return (
            jsonify({"success": False, "output": f"Comando não reconhecido: {cmd}"}),
            400,
        )
    except Exception as e:
        return jsonify({"success": False, "output": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

"""
Cliente HTTP para interagir com o Flask API
Pode ser usado pelo CLI ou outras aplicações
"""

import requests
import json
from typing import Dict, List, Optional, Any


class FlaskClient:
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    def is_online(self) -> bool:
        """Verifica se o servidor Flask está online"""
        try:
            response = self.session.get(f"{self.base_url}/api/status", timeout=2)
            return response.status_code == 200
        except Exception:
            return False

    # =============== TASKS ===============

    def get_all_tasks(self) -> Optional[List[Dict]]:
        """Retorna todas as tarefas"""
        try:
            response = self.session.get(f"{self.base_url}/api/tasks")
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Erro ao listar tarefas: {e}")
            return None

    def get_task(self, task_id: int) -> Optional[Dict]:
        """Retorna uma tarefa específica"""
        try:
            response = self.session.get(f"{self.base_url}/api/tasks/{task_id}")
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Erro ao buscar tarefa: {e}")
            return None

    def create_task(
        self,
        title: str,
        description: str = "",
        status: str = "pending",
        priority: int = 1,
    ) -> Optional[Dict]:
        """Cria uma nova tarefa"""
        try:
            data = {
                "title": title,
                "description": description,
                "status": status,
                "priority": priority,
            }
            response = self.session.post(
                f"{self.base_url}/api/tasks",
                json=data,
                headers={"Content-Type": "application/json"},
            )
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Erro ao criar tarefa: {e}")
            return None

    def update_task(
        self,
        task_id: int,
        title: str,
        description: str = "",
        status: str = "pending",
        priority: int = 1,
    ) -> Optional[Dict]:
        """Atualiza uma tarefa"""
        try:
            data = {
                "title": title,
                "description": description,
                "status": status,
                "priority": priority,
            }
            response = self.session.put(
                f"{self.base_url}/api/tasks/{task_id}",
                json=data,
                headers={"Content-Type": "application/json"},
            )
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Erro ao atualizar tarefa: {e}")
            return None

    def delete_task(self, task_id: int) -> Optional[Dict]:
        """Deleta uma tarefa"""
        try:
            response = self.session.delete(f"{self.base_url}/api/tasks/{task_id}")
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Erro ao deletar tarefa: {e}")
            return None

    def mark_task_done(self, task_id: int) -> Optional[Dict]:
        """Marca uma tarefa como concluída"""
        task = self.get_task(task_id)
        if task:
            return self.update_task(
                task_id,
                title=task.get("title", ""),
                description=task.get("description", ""),
                status="done",
                priority=task.get("priority", 1),
            )
        return None

    def mark_task_in_progress(self, task_id: int) -> Optional[Dict]:
        """Marca uma tarefa como em progresso"""
        task = self.get_task(task_id)
        if task:
            return self.update_task(
                task_id,
                title=task.get("title", ""),
                description=task.get("description", ""),
                status="in_progress",
                priority=task.get("priority", 1),
            )
        return None

    # =============== FILES ===============

    def upload_file(self, file_path: str) -> Optional[Dict]:
        """Faz upload de um arquivo e processa"""
        try:
            with open(file_path, "rb") as file:
                files = {"file": (file_path.split("/")[-1], file)}
                response = self.session.post(f"{self.base_url}/api/upload", files=files)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Erro ao fazer upload: {e}")
            return None

    def get_processed_files(self) -> Optional[List[Dict]]:
        """Retorna arquivos processados"""
        try:
            response = self.session.get(f"{self.base_url}/api/processed-files")
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Erro ao listar arquivos processados: {e}")
            return None

    # =============== EXPORT ===============

    def export_tasks_to_xlsx(self, output_path: str = "tasks_export.xlsx") -> bool:
        """Exporta tarefas para arquivo XLSX"""
        try:
            response = self.session.get(f"{self.base_url}/api/export/tasks")
            if response.status_code == 200:
                with open(output_path, "wb") as f:
                    f.write(response.content)
                print(f"✅ Arquivo exportado: {output_path}")
                return True
            return False
        except Exception as e:
            print(f"Erro ao exportar tarefas: {e}")
            return False

    # =============== STATUS ===============

    def get_status(self) -> Optional[Dict]:
        """Retorna status do servidor"""
        try:
            response = self.session.get(f"{self.base_url}/api/status")
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Erro ao buscar status: {e}")
            return None


# Função helper para uso direto
def create_client(base_url: str = "http://localhost:5000") -> FlaskClient:
    """Cria e retorna uma instância do cliente"""
    return FlaskClient(base_url)


if __name__ == "__main__":
    # Teste rápido
    client = FlaskClient()

    if client.is_online():
        print("✅ Servidor Flask está online!")
        status = client.get_status()
        print(f"Status: {status}")
    else:
        print("❌ Servidor Flask não está respondendo. Inicie-o com: python main.py")

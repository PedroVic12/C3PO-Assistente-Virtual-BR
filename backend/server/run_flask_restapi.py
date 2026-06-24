#!/usr/bin/env python3
"""
EXEMPLO DE USO: Integração Flask + Notificações com TTS
Demonstra como criar tarefas e ver as notificações em tempo real
"""

import time
from flask_client import create_client


def main():
    print("\n" + "=" * 70)
    print("🎯 EXEMPLO DE USO: INTEGRAÇÃO FLASK + NOTIFICAÇÕES")
    print("=" * 70)

    # Criar cliente
    client = create_client("http://localhost:5000")

    # Verificar se Flask está online
    if not client.is_online():
        print("\n❌ Erro: Flask não está respondendo!")
        print("   Execute em outro terminal: python main.py")
        return

    print("\n✅ Conectado ao servidor Flask!")

    # 1. Criar uma tarefa simples
    print("\n" + "-" * 70)
    print("1️⃣  CRIANDO TAREFA")
    print("-" * 70)

    tasks = [
        {
            "title": "Revisar documentação técnica",
            "description": "Revisar o guia de implementação do RCE",
            "priority": 2,
        },
        {
            "title": "Testar integração Flask",
            "description": "Criar tarefa de teste para verificar notificações",
            "priority": 1,
        },
        {
            "title": "Exportar tarefas para Excel",
            "description": "Testar funcionalidade de exportação",
            "priority": 3,
        },
        {
            "title": "Verificar status do servidor",
            "description": "Checar endpoint de status para monitoramento",
            "priority": 2,
        },
    ]

    for task in tasks:
        resultado = client.create_task(**task)

    if resultado and resultado.get("success"):
        task_id = resultado.get("id")
        print(f"✅ Tarefa criada com sucesso!")
        print(f"   ID: {task_id}")
        print(f"   Mensagem: {resultado.get('message')}")
        print("   🔔 Você deve ter ouvido uma notificação!")
    else:
        print(f"❌ Erro ao criar tarefa: {resultado}")
        return

    time.sleep(2)

    # 2. Listar tarefas
    print("\n" + "-" * 70)
    print("2️⃣  LISTANDO TAREFAS")
    print("-" * 70)

    tarefas = client.get_all_tasks()
    if tarefas:
        print(f"Total de tarefas: {len(tarefas)}\n")
        for tarefa in tarefas:
            status_emoji = {"pending": "⏳", "in_progress": "🔄", "done": "✅"}.get(
                tarefa["status"], "❓"
            )

            print(f"{status_emoji} ID {tarefa['id']}: {tarefa['title']}")
            print(f"   Status: {tarefa['status']} | Prioridade: {tarefa['priority']}")
            if tarefa["description"]:
                print(f"   Descrição: {tarefa['description']}")
            print()

    time.sleep(2)

    # 3. Atualizar tarefa
    print("-" * 70)
    print("3️⃣  ATUALIZANDO TAREFA")
    print("-" * 70)

    resultado = client.update_task(
        task_id=task_id,
        title="Revisar documentação técnica (REVISADO)",
        description="Já foi revisado e aprovado",
        status="done",
        priority=2,
    )

    if resultado and resultado.get("success"):
        print(f"✅ Tarefa atualizada!")
        print(f"   Mensagem: {resultado.get('message')}")
        print("   🔔 Você deve ter ouvido outra notificação!")
    else:
        print(f"❌ Erro: {resultado}")

    time.sleep(2)

    # 4. Exportar tarefas
    print("\n" + "-" * 70)
    print("4️⃣  EXPORTANDO TAREFAS PARA EXCEL")
    print("-" * 70)

    export_file = "exemplo_tarefas_export.xlsx"
    sucesso = client.export_tasks_to_xlsx(export_file)

    if sucesso:
        print(f"✅ Exportado para: {export_file}")
    else:
        print("❌ Erro ao exportar")

    time.sleep(1)

    # 5. Verificar status do servidor
    print("\n" + "-" * 70)
    print("5️⃣  STATUS DO SERVIDOR")
    print("-" * 70)

    status = client.get_status()
    if status:
        print(f"✅ Status: {status['status']}")
        print(f"   Tarefas: {status['tasks_count']}")
        print(f"   Arquivos processados: {status['files_count']}")
        print(f"   Timestamp: {status['timestamp']}")

    print("\n" + "=" * 70)
    print("✨ EXEMPLO COMPLETO! INTEGRAÇÃO FUNCIONANDO!")
    print("=" * 70)
    print("\n📚 Para aprender mais:")
    print("   - Ver README.md para documentação completa")
    print("   - Ver flask_client.py para todas as funções disponíveis")
    print("   - Ver main.py para endpoints das APIs")
    print()


if __name__ == "__main__":
    main()

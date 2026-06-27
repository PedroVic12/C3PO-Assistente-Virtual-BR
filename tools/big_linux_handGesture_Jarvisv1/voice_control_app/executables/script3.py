import time

def main():
    print("Executando Script 3")
    print("Processando dados de equipamentos...")
    stages = ["Calibração", "Verificação", "Validação"]
    for stage in stages:
        print(f"Executando {stage}...")
        time.sleep(1)
    print("Processamento finalizado!")

if __name__ == "__main__":
    main()

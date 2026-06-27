import time

def main():
    print("Executando Script 1")
    print("Realizando análise de dados oceanográficos...")
    for i in range(5):
        print(f"Progresso: {(i+1)*20}%")
        time.sleep(1)
    print("Análise concluída!")

if __name__ == "__main__":
    main()

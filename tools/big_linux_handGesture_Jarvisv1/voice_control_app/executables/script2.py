import time

def main():
    print("Executando Script 2")
    print("Gerando relatório de campanhas...")
    for i in range(3):
        print(f"Gerando seção {i+1}/3...")
        time.sleep(1)
    print("Relatório gerado com sucesso!")

if __name__ == "__main__":
    main()

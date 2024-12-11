import pyautogui
import time

# Função para capturar as coordenadas do mouse em tempo real
def capturar_coordenadas():
    print("Clique em qualquer lugar para capturar as coordenadas do mouse. Pressione Ctrl+C para sair.")
    try:
        while True:
            # Aguardar um clique e capturar a posição do mouse
            x, y = pyautogui.position()
            print(f"Posição atual do mouse: X={x}, Y={y}", end="\r", flush=True)
            time.sleep(0.1)  # Intervalo curto para não sobrecarregar o console
    except KeyboardInterrupt:
        print("\nCaptura encerrada.")

# Função para simular scroll
def realizar_scroll(direcao, quantidade):
    """
    Realiza o scroll na página.
    :param direcao: "up" para cima ou "down" para baixo
    :param quantidade: número de "scrolls" a realizar
    """
    if direcao == "up":
        pyautogui.scroll(quantidade)
    elif direcao == "down":
        pyautogui.scroll(-quantidade)
    else:
        print("Direção inválida. Use 'up' ou 'down'.")

# Função para clicar em um botão após capturar as coordenadas
def clicar_botao(x, y, delay=1):
    """
    Move o mouse para as coordenadas especificadas e clica.
    :param x: Coordenada X do botão
    :param y: Coordenada Y do botão
    :param delay: Tempo em segundos para esperar antes de clicar
    """
    print(f"Movendo para X={x}, Y={y} e clicando...")
    pyautogui.moveTo(x, y, duration=delay)
    pyautogui.click()
    print("Clique realizado!")

# Exemplo de uso
if __name__ == "__main__":
    print("=== Automação Iniciada ===")
    print("Escolha uma opção:")
    print("1. Capturar coordenadas do mouse")
    print("2. Realizar scroll")
    print("3. Clicar em um botão")
    print("4. Sair")

    while True:
        escolha = input("Digite sua escolha (1/2/3/4): ")

        if escolha == "1":
            capturar_coordenadas()
        elif escolha == "2":
            direcao = input("Digite a direção do scroll ('up' ou 'down'): ").strip().lower()
            quantidade = int(input("Digite a quantidade de scrolls: "))
            realizar_scroll(direcao, quantidade)
        elif escolha == "3":
            x = int(input("Digite a coordenada X do botão: "))
            y = int(input("Digite a coordenada Y do botão: "))
            delay = float(input("Digite o tempo de espera antes de clicar (em segundos): "))
            clicar_botao(x, y, delay)
        elif escolha == "4":
            print("Encerrando o programa.")
            break
        else:
            print("Escolha inválida. Tente novamente.")

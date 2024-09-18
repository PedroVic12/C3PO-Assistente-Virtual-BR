from manim import *

class Intro(Scene):
    def construct(self):
        # Círculo maior com preenchimento roxo
        c = Circle(3, color=RED, fill_color=PURPLE, fill_opacity=0.3)
        self.play(DrawBorderThenFill(c), run_time=0.5)

        # Título e subtítulo em branco
        title = Text("Jedi CyberPunk", font="Arial", font_size=40, color=YELLOW).shift(UP*0.5)
        #subtittle = Text("A New Hope", font="Arial", font_size=40, color=WHITE).shift(DOWN * 0.25)
        assunto = Text("O que é IA em 2024?", font="Arial", font_size=40, color=WHITE).shift(DOWN * 0.9)

        # Centraliza os textos no círculo
        self.play(Write(title), 
                  #Write(subtittle), 
                  Write(assunto))

        # Arco completo em torno do círculo (Círculo completo)
        a = Arc(radius=3.3, angle=TAU, color=BLUE, stroke_width=15)
        self.play(Create(a))

        # Pausa para visualização
        self.wait(2)

        # Desvanecimento dos textos
        self.play(FadeOut(title), 
                  #FadeOut(subtittle), 
                  FadeOut(assunto))


# Comando para salvar o vídeo em um diretório específico (output/)
if __name__ == "__main__":
    config.media_dir = "/home/pedrov12/Documentos/GitHub/C3PO-Assistente-Virtual-BR/system_editor_gaveta/animations/output"  # Define o diretório de saída
    scene = Intro()
    scene.render()  # Gera e renderiza o vídeo

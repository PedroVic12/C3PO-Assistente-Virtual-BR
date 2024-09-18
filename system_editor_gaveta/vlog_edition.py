from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, TextClip

class VideoEditorWithImagesAndText:
    def __init__(self, video_file, output_file, fps=24):
        self.video_file = video_file
        self.output_file = output_file
        self.fps = fps
        self.video_clip = VideoFileClip(self.video_file)
        self.clips = [self.video_clip]  # O vídeo de fundo é o primeiro clip

    def add_image_to_video(self, image_path, start_time, end_time, position):
        """
        Adiciona uma imagem sobre o vídeo com a duração e posição especificadas.
        :param image_path: Caminho da imagem
        :param start_time: Início de exibição da imagem no vídeo (em segundos)
        :param end_time: Fim de exibição da imagem no vídeo (em segundos)
        :param position: (x, y) - Coordenadas da posição da imagem sobre o vídeo
        """
        duration = end_time - start_time
        image_clip = (ImageClip(image_path)
                      .set_duration(duration)
                      .set_position(position)
                      .set_start(start_time))
        self.clips.append(image_clip)

    def add_gif_to_video(self, gif_path, start_time, end_time, position):
        """
        Adiciona um GIF animado sobre o vídeo com a duração e posição especificadas.
        :param gif_path: Caminho do GIF
        :param start_time: Início de exibição do GIF no vídeo (em segundos)
        :param end_time: Fim de exibição do GIF no vídeo (em segundos)
        :param position: (x, y) - Coordenadas da posição do GIF sobre o vídeo
        """
        duration = end_time - start_time
        gif_clip = (VideoFileClip(gif_path)
                    .subclip(0, duration)
                    .set_position(position)
                    .set_start(start_time))
        self.clips.append(gif_clip)

    def add_text_to_video(self, text, start_time, end_time, position, fontsize=50, color='white', font='Arial'):
        """
        Adiciona um texto sobre o vídeo com a duração e posição especificadas.
        :param text: Texto a ser adicionado
        :param start_time: Início de exibição do texto no vídeo (em segundos)
        :param end_time: Fim de exibição do texto no vídeo (em segundos)
        :param position: (x, y) - Coordenadas da posição do texto sobre o vídeo
        :param fontsize: Tamanho da fonte
        :param color: Cor do texto
        :param font: Fonte do texto
        """
        duration = end_time - start_time
        text_clip = (TextClip(text, fontsize=fontsize, color=color, font=font)
                     .set_duration(duration)
                     .set_position(position)
                     .set_start(start_time))
        self.clips.append(text_clip)

    def create_final_video(self):
        """Cria o vídeo final com todas as imagens e textos sobrepostos ao vídeo de fundo."""
        final_clip = CompositeVideoClip(self.clips)
        final_clip.write_videofile(self.output_file, codec="libx264", fps=self.fps)
        print(f"Vídeo final salvo em {self.output_file}")


# Exemplo de uso
if __name__ == "__main__":
    path = "/home/pedrov12/Documentos/GitHub/C3PO-Assistente-Virtual-BR/system_editor_gaveta/imagens"
    output_file = f"/home/pedrov12/Documentos/GitHub/C3PO-Assistente-Virtual-BR/system_editor_gaveta/output/video_final.mp4"
    video_file = "/home/pedrov12/Downloads/new-ia-the-age2024_bvsoVoax.mp4"
    img_path = "/home/pedrov12/Imagens/"
    videos_path = "/home/pedrov12/Vídeos/"

    video_file = "/home/pedrov12/Downloads/IA_the_age2024.mp4"

    
    # Criação do editor de vídeo
    editor = VideoEditorWithImagesAndText(video_file, output_file)

    # Conversão de minutos e segundos para segundos absolutos
    def time_in_seconds(minutes, seconds):
        return minutes * 60 + seconds

    # Adicionando imagens e textos manualmente
    editor.add_text_to_video("Explicação sobre o App Service", 
                             start_time=time_in_seconds(2, 15), 
                             end_time=time_in_seconds(2, 30), 
                             position=("left", 'top'), 
                             fontsize=40, color='white')
    editor.add_gif_to_video(f"{videos_path}/ficando_feliz.gif", 
                              start_time=time_in_seconds(2, 15), 
                              end_time=time_in_seconds(2, 30), 
                              position=("left", 'center'))  # Posição esquerda

    # Exemplo: de 4min10s a 4min30s (250s a 270s) com a imagem e texto à direita
    editor.add_text_to_video("Explicação sobre o Dashboard", 
                             start_time=time_in_seconds(4, 10), 
                             end_time=time_in_seconds(4, 30), 
                             position=('left', 'top'), 
                             fontsize=40, color='blue')

    editor.add_image_to_video(f"{path}/dash.png", 
                              start_time=time_in_seconds(4, 10), 
                              end_time=time_in_seconds(4, 30), 
                              position=('left', 'center'))  # Posição direita

    
    # Criar o vídeo final
    editor.create_final_video()

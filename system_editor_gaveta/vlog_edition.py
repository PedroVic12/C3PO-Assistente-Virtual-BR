from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip

class VideoEditorWithImages:
    def __init__(self, video_file, output_file, fps=24):
        self.video_file = video_file
        self.output_file = output_file
        self.fps = fps
        self.video_clip = VideoFileClip(self.video_file)
        self.clips = [self.video_clip]  # O vídeo de fundo é o primeiro clip

    def input_image_on_video(self, image_path, times, position):
        """
        Adiciona uma imagem sobre o vídeo com a duração e posição especificadas.
        
        :param image_path: Caminho da imagem
        :param times: [start_time, end_time] - Duração de exibição da imagem no vídeo
        :param position: (x, y) - Coordenadas da posição da imagem sobre o vídeo
        """
        start_time, end_time = times
        duration = end_time - start_time

        # Cria o ImageClip com a duração apropriada
        image_clip = ImageClip(image_path).set_duration(duration).set_position(position).set_start(start_time)
        
        # Ajusta o tamanho da imagem ao tamanho do vídeo
        #image_clip = image_clip.resize(height=self.video_clip.h)  # Ajusta a altura da imagem para o vídeo
        
        # Adiciona o clip de imagem à lista de clips
        self.clips.append(image_clip)
    
    def create_final_video(self):
        """Cria o vídeo final com todas as imagens sobrepostas ao vídeo de fundo."""
        final_clip = CompositeVideoClip(self.clips)
        final_clip.write_videofile(self.output_file, codec="libx264", fps=self.fps)
        print(f"Vídeo final salvo em {self.output_file}")

# Parâmetros para o editor de vídeo
path = r"/home/pedrov12/Documentos/GitHub/C3PO-Assistente-Virtual-BR/system_editor_gaveta/imagens"

video_file = "C3PO-Assistente-Virtual-BR/system_editor_gaveta/videos/kanban_project.mp4"
output_file = f"{path}/video_final_com_imagens.mp4"


# Criação do editor de vídeo
editor = VideoEditorWithImages(video_file, output_file)

# Exemplo de imagens sobrepostas ao vídeo
# 1ª Imagem: Na esquerda, aparece de 1.15s a 11.15s
editor.input_image_on_video(f"/home/pedrov12/Documentos/GitHub/C3PO-Assistente-Virtual-BR/system_editor_gaveta/imagens/app_service.jpg", [1.15, 11.15], position=(editor.video_clip.w + 200, 'center'))

# 2ª Imagem: Na direita, aparece de 11.15s a 16.15s
editor.input_image_on_video(f"{path}/dash.png", [11.15, 16.15], position=(editor.video_clip.w - 200, 'center'))

# 3ª Imagem: Ocupa ambas as laterais (centro), aparece de 16.15s a 21.15s
editor.input_image_on_video(f"{path}/chabot_service.jpg", [16.15, 21.15], position=('center', 'center'))

# Criar o vídeo final
editor.create_final_video()

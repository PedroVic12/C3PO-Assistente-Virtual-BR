from mutagen.mp3 import MP3
from PIL import Image
from pathlib import Path
import os
import imageio
#from moviepy import VideoFileClip, TextClip, CompositeVideoClip
import moviepy as editor


class AudioToVideoConverter:
    def __init__(self, audio_path: str, images_path: str, video_output_path: str):
        self.audio_path = audio_path
        self.images_path = images_path
        self.video_output_path = video_output_path
        self.audio_length = None
        self.list_of_images = []
        self.gif_path = "images.gif"

    def get_audio_length(self):
        """Carrega o áudio e obtém sua duração."""
        audio = MP3(self.audio_path)
        self.audio_length = audio.info.length
        print(f"Duração do áudio: {self.audio_length} segundos.")

    def process_images(self, size=(400, 400)):
        """Carrega, redimensiona e prepara as imagens."""
        print("Processando imagens...")
        for image_file in os.listdir(self.images_path):
            if image_file.endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(self.images_path, image_file)
                image = Image.open(image_path).resize(size, Image.Resampling.LANCZOS)
                self.list_of_images.append(image)
        print(f"{len(self.list_of_images)} imagens processadas.")

    def create_gif(self):
        """Cria um GIF a partir das imagens processadas."""
        if not self.list_of_images:
            raise ValueError("Nenhuma imagem foi processada.")
            if self.audio_length is None:
                raise ValueError("Could not determine audio length")
            duration = self.audio_length / len(self.list_of_images)
            imageio.mimsave(self.gif_path, self.list_of_images, fps=1 / duration)
        print(f"GIF criado em: {self.gif_path}")

    def create_video(self, fps=60):
        """Combina o GIF com o áudio para criar um vídeo final."""
        print("Criando vídeo...")
        video = editor.VideoFileClip(self.gif_path)
        audio = editor.AudioFileClip(self.audio_path)
        final_video = video.set_audio(audio)  # Corrected line

        # Salvar o vídeo final no diretório especificado
        os.makedirs(self.video_output_path, exist_ok=True)
        output_path = os.path.join(self.video_output_path, "video.mp4")
        final_video.write_videofile(output_path, fps=fps, codec="libx264", audio_codec='aac')
        print(f"Vídeo final salvo em: {output_path}")







    def convert(self):
        """Executa todas as etapas para converter áudio e imagens em um vídeo."""
        self.get_audio_length()
        self.process_images()
        self.create_gif()
        self.create_video()


# Uso da classe
if __name__ == "__main__":
    # Caminhos dos arquivos
    audio_path = os.path.join(os.getcwd(), "audio.mp3")
    images_path = os.path.join(os.getcwd(), "imagens")
    video_path = os.path.join(os.getcwd(), "videos")

    # Criar instância da classe e executar o processo de conversão
    converter = AudioToVideoConverter(audio_path, images_path, video_path)
    converter.convert()

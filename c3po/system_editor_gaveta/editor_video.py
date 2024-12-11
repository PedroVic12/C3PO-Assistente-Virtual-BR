from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, concatenate_videoclips
import os

class VideoEditor:
    def __init__(self, video_folder, image_folder, output_file, image_duration=3, fade_duration=1):
        self.video_folder = video_folder
        self.image_folder = image_folder
        self.output_file = output_file
        self.image_duration = image_duration
        self.fade_duration = fade_duration
        self.clips = []

    def load_videos(self):
        """Carrega todos os vídeos da pasta especificada."""
        for filename in sorted(os.listdir(self.video_folder)):
            if filename.endswith(".mp4"):
                video_path = os.path.join(self.video_folder, filename)
                video_clip = VideoFileClip(video_path)
                self.clips.append(video_clip)
    
    def load_images(self):
        """Carrega todas as imagens e aplica animação de fade in/out."""
        for filename in sorted(os.listdir(self.image_folder)):
            if filename.endswith((".jpg", ".png")):
                image_path = os.path.join(self.image_folder, filename)
                image_clip = ImageClip(image_path).set_duration(self.image_duration)
                image_clip = image_clip.crossfadein(self.fade_duration).crossfadeout(self.fade_duration)
                self.clips.append(image_clip)
    
    def create_final_video(self):
        """Cria o vídeo final com todas as imagens e vídeos em sequência."""
        final_clip = concatenate_videoclips(self.clips, method="compose")
        final_clip.write_videofile(self.output_file, codec="libx264", fps=24)
        print(f"Vídeo salvo em {self.output_file}")

# Parâmetros para o editor de vídeo
video_folder = "videos/"
image_folder = "imagens/"
output_file = "meu_video_jedi.mp4"

# Criação do editor de vídeo
editor = VideoEditor(video_folder, image_folder, output_file)
editor.load_videos()  # Carrega os vídeos
editor.load_images()  # Carrega as imagens
editor.create_final_video()  # Cria o vídeo final

#!/usr/bin/env python3
"""
Annotate Kanban Demo Video:
Uses moviepy to load 'kanban_project.mp4' and overlay annotations
showcasing the key features of the project (Sync, Excel, Obsidian).
"""

import os
import sys

# Use moviepy v2.x import style
try:
    from moviepy import VideoFileClip, TextClip, CompositeVideoClip
except ImportError:
    print("Por favor, instale o moviepy antes: pip install moviepy --break-system-packages")
    sys.exit(1)

def main():
    video_dir = "/home/pedrov12/Documentos/GitHub/C3PO-Assistente-Virtual-BR/c3po/system_editor_gaveta/videos"
    video_path = os.path.join(video_dir, "kanban_project.mp4")
    output_path = os.path.join(video_dir, "kanban_project_annotated.mp4")

    if not os.path.exists(video_path):
        print(f"Erro: Vídeo original não encontrado em {video_path}")
        sys.exit(1)

    font_path = "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf"
    if not os.path.exists(font_path):
        font_path = None  # fallback

    print("Carregando clipe original...")
    clip = VideoFileClip(video_path)
    
    print("Criando sobreposições de texto...")
    
    # Title at the beginning (0s to 5s)
    txt_title = (TextClip(
        text="BATCAVERNA 2026: KANBAN PRO",
        font=font_path,
        font_size=48,
        color="cyan"
    )
    .with_duration(5)
    .with_position(("center", 60))
    .with_start(0))

    # Feature 1 (5s to 12s)
    txt_feat1 = (TextClip(
        text="Sincronização Bidirecional (NextJS + Excel)",
        font=font_path,
        font_size=36,
        color="white"
    )
    .with_duration(7)
    .with_position(("center", 80))
    .with_start(5))

    # Feature 2 (12s to 19s)
    txt_feat2 = (TextClip(
        text="Integração Direta com Notas do Obsidian (Markdown)",
        font=font_path,
        font_size=36,
        color="lightgreen"
    )
    .with_duration(7)
    .with_position(("center", 80))
    .with_start(12))

    # Ending (19s to end)
    txt_end = (TextClip(
        text="Desenvolvido por Pedro Victor Veras",
        font=font_path,
        font_size=40,
        color="yellow"
    )
    .with_duration(clip.duration - 19)
    .with_position(("center", clip.size[1] - 100))
    .with_start(19))

    print("Compondo o vídeo final...")
    annotated_clip = CompositeVideoClip([clip, txt_title, txt_feat1, txt_feat2, txt_end])
    
    print("Renderizando vídeo (isso pode levar alguns instantes)...")
    annotated_clip.write_videofile(
        output_path,
        fps=24,
        codec="libx264"
    )
    
    print(f"Vídeo final renderizado e salvo com sucesso em: {output_path}")

if __name__ == "__main__":
    main()

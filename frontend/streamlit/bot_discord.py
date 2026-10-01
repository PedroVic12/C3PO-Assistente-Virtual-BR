import asyncio
import os
import random
from urllib.parse import urlparse

import aiohttp
import discord
import yt_dlp
from discord import app_commands
from discord.ext import commands

#! pip install discord yt_dlp aiohttp --break-system-packages


permissoes = discord.Intents.default()
permissoes.message_content = True

bot = commands.Bot(command_prefix="!", intents=permissoes)
adivinhacoes: dict[tuple[int | None, int], dict[str, int]] = {}

piadas = [
    "Por que o livro de matemática ficou triste? Porque tinha muitos problemas.",
    "O que o zero disse para o oito? Belo cinto!",
    "Qual é o contrário de volátil? Vem cá, sobrinho.",
    "Por que o computador foi ao médico? Porque estava com um vírus.",
    "O que o tomate foi fazer no banco? Tirar extrato.",
]

YDL_OPTIONS = {
    "format": "bestaudio/best",
    "quiet": True,
    "no_warnings": True,
    "noplaylist": True,
    "default_search": "auto",
}


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot {bot.user} está online e pronto para uso!")


@bot.command(name="sincronizar")
async def sincronizar(ctx: commands.Context):
    owner_id = os.getenv("DISCORD_OWNER_ID")
    if owner_id and ctx.author.id == int(owner_id):
        comandos = await bot.tree.sync()
        await ctx.reply(f"{len(comandos)} comandos sincronizados com sucesso!")
    else:
        await ctx.reply("Você não tem permissão para sincronizar os comandos do bot.")


@bot.tree.command(description="Diz olá ao usuário")
async def ola(interaction: discord.Interaction):
    canal = interaction.channel.mention if interaction.channel else "este canal"
    await interaction.response.send_message(
        f"Olá {interaction.user.name}! Bem-vindo ao canal {canal}. Como posso ajudá-lo hoje?"
    )


@bot.tree.command(description="Soma dois números")
@app_commands.describe(num1="Primeiro número", num2="Segundo número")
async def somar(interaction: discord.Interaction, num1: int, num2: int):
    await interaction.response.send_message(f"A soma de {num1} e {num2} é {num1 + num2}.")


@bot.tree.command(description="Envia uma mensagem para o canal")
@app_commands.describe(frase="Mensagem que será enviada")
async def falar(interaction: discord.Interaction, frase: str):
    await interaction.response.send_message(f"Mensagem enviada: {frase}")
    if interaction.channel:
        await interaction.channel.send(f"{interaction.user.name} disse: {frase}")


@bot.tree.command(description="Toca uma música do YouTube no seu canal de voz")
@app_commands.describe(url="URL de um vídeo do YouTube")
async def tocar(interaction: discord.Interaction, url: str):
    endereco = urlparse(url)
    if endereco.scheme not in {"http", "https"} or endereco.netloc.lower() not in {
        "youtube.com",
        "www.youtube.com",
        "m.youtube.com",
        "music.youtube.com",
        "youtu.be",
        "www.youtu.be",
    }:
        await interaction.response.send_message("Envie uma URL válida do YouTube.", ephemeral=True)
        return

    if not interaction.guild or not isinstance(interaction.user, discord.Member):
        await interaction.response.send_message("Este comando só pode ser usado em um servidor.", ephemeral=True)
        return

    canal_voz = interaction.user.voice.channel if interaction.user.voice else None
    if not canal_voz:
        await interaction.response.send_message("Entre em um canal de voz primeiro.", ephemeral=True)
        return

    await interaction.response.defer(thinking=True)
    try:
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as extrator:
            info = await asyncio.to_thread(extrator.extract_info, url, download=False)
        if "entries" in info:
            info = next((item for item in info["entries"] if item), None)
        audio_url = info.get("url") if info else None
        if not audio_url:
            raise ValueError("Não foi possível obter o áudio deste vídeo.")
    except Exception as erro:
        await interaction.followup.send(f"Não consegui abrir esse vídeo: {erro}", ephemeral=True)
        return

    conexao = interaction.guild.voice_client
    if conexao and conexao.is_connected():
        if conexao.channel != canal_voz:
            await conexao.move_to(canal_voz)
        if conexao.is_playing():
            conexao.stop()
    else:
        conexao = await canal_voz.connect()

    fonte = discord.FFmpegPCMAudio(
        audio_url,
        before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
        options="-vn",
    )
    conexao.play(fonte)
    await interaction.followup.send(f"Tocando agora: **{info.get('title', 'Vídeo do YouTube')}**")


@bot.tree.command(description="Envia um meme aleatório")
async def meme(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    try:
        timeout = aiohttp.ClientTimeout(total=15)
        async with aiohttp.ClientSession(timeout=timeout) as sessao:
            async with sessao.get("https://meme-api.com/gimme") as resposta:
                resposta.raise_for_status()
                dados = await resposta.json()
        embed = discord.Embed(title=dados.get("title", "Meme aleatório"), color=discord.Color.gold())
        embed.set_image(url=dados["url"])
        await interaction.followup.send(embed=embed)
    except (aiohttp.ClientError, KeyError, ValueError):
        await interaction.followup.send("Não consegui buscar um meme agora. Tente novamente mais tarde.")


@bot.tree.command(description="Conta uma piada aleatória")
async def piada(interaction: discord.Interaction):
    await interaction.response.send_message(random.choice(piadas))


@bot.tree.command(description="Começa um jogo de adivinhar o número")
async def adivinhar(interaction: discord.Interaction):
    chave = (interaction.guild_id, interaction.user.id)
    adivinhacoes[chave] = {"numero": random.randint(1, 100), "tentativas": 0}
    await interaction.response.send_message(
        "Pensei em um número de 1 a 100. Use `/chutar` para tentar adivinhar!", ephemeral=True
    )


@bot.tree.command(description="Tenta adivinhar o número secreto")
@app_commands.describe(numero="Seu palpite, de 1 a 100")
async def chutar(interaction: discord.Interaction, numero: int):
    if not 1 <= numero <= 100:
        await interaction.response.send_message("Escolha um número de 1 a 100.", ephemeral=True)
        return

    chave = (interaction.guild_id, interaction.user.id)
    jogo = adivinhacoes.get(chave)
    if not jogo:
        await interaction.response.send_message("Comece uma partida com `/adivinhar`.", ephemeral=True)
        return

    jogo["tentativas"] += 1
    if numero == jogo["numero"]:
        tentativas = jogo["tentativas"]
        del adivinhacoes[chave]
        await interaction.response.send_message(
            f"Acertou! O número era **{numero}**. Você conseguiu em {tentativas} tentativa(s)!",
            ephemeral=True,
        )
    elif numero < jogo["numero"]:
        await interaction.response.send_message("O número secreto é maior. Tente de novo!", ephemeral=True)
    else:
        await interaction.response.send_message("O número secreto é menor. Tente de novo!", ephemeral=True)


if __name__ == "__main__":
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        raise RuntimeError("Defina a variável de ambiente DISCORD_BOT_TOKEN antes de iniciar o bot.")
    bot.run(token)
import os
from telebot import TeleBot
import ffmpeg

TOKEN = '7818202477:AAFMtkbVArjNrpELEMIwSldV76j8iF49Cos'  # Substitua YOUR_TOKEN pelo token do BotFather
bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Envie um vídeo para converter para GBA!')

@bot.message_handler(content_types=['video'])
def convert_video(message):
    # Baixar o vídeo
    video_file = bot.download_file(message.video.file_id)
    with open('input.mp4', 'wb') as f:
        f.write(video_file)

    # Converter para formato compatível com GBA
    stream = ffmpeg.input('input.mp4')
    stream = ffmpeg.output(stream, 'output.gba', video_bitrate='500k', s='240x160', r=10)
    ffmpeg.run(stream)

    # Enviar de volta ao usuário
    with open("output.gba", 'rb') as converted_video:
        bot.send_document(message.chat.id, converted_video)

    # Limpar arquivos temporários
    os.remove("input.mp4")
    os.remove("output.gba")

# Iniciar o bot
bot.polling()

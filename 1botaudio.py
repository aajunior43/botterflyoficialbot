import logging
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from gtts import gTTS
import os

# Ative o logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Token do Bot do Telegram
TOKEN = "6081911245:AAFXOtmqUIT18EVXiGPcfoth7C3VKDl_0ic"

def start(update: Update, _: CallbackContext) -> None:
    """Envia uma mensagem quando o comando /start é emitido."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Olá {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )

def audio(update: Update, context: CallbackContext) -> None:
    """Cria um arquivo de áudio a partir do texto enviado e o envia."""
    text = ' '.join(context.args)
    tts = gTTS(text=text, lang='pt')
    audio_file = 'text_to_audio.mp3'
    tts.save(audio_file)
    with open(audio_file, 'rb') as f:
        context.bot.send_audio(chat_id=update.effective_chat.id, audio=f)
    os.remove(audio_file)

def main() -> None:
    """Inicie o bot."""
    updater = Updater(token=TOKEN)

    # Obtenha o despachante para registrar manipuladores
    dispatcher = updater.dispatcher

    # Comandos
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("audio", audio))

    # Inicie o Bot
    updater.start_polling()

    # Bloqueie até que você interrompa o bot (por exemplo, quando pressiona Ctrl + C em sua linha de comando).
    updater.idle()

if __name__ == '__main__':
    main()

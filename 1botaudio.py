from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, CallbackContext
from gtts import gTTS
import os

TOKEN = "6081911245:AAFXOtmqUIT18EVXiGPcfoth7C3VKDl_0ic"

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Olá {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )

def audio(update: Update, context: CallbackContext) -> None:
    text = ' '.join(context.args)
    tts = gTTS(text=text, lang='pt')
    audio_file = 'text_to_audio.mp3'
    tts.save(audio_file)
    with open(audio_file, 'rb') as f:
        context.bot.send_audio(chat_id=update.effective_chat.id, audio=f)
    os.remove(audio_file)
    
    try:
        context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
    except Exception as e:
        print(f"Erro ao apagar a mensagem: {e}")

def main() -> None:
    updater = Updater(token=TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("audio", audio))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
    

from telegram import Update, Bot
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackContext
from mega import Mega
import logging

# Ative o log
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

logger = logging.getLogger(__name__)

# Credenciais do Mega
MEGA_EMAIL = 'aajunior43@gmail.com'
MEGA_PASSWORD = 'Jr19991020.'

mega = Mega()
m = mega.login(MEGA_EMAIL, MEGA_PASSWORD)

# Iniciar o Bot
TOKEN = '6139212717:AAEFn37NwYuKIS8BXotVNXHVYzG4L9FOSWA'
bot = Bot(token=TOKEN)
updater = Updater(bot=bot, use_context=True)

# Manejador para documentos enviados
def document_handler(update: Update, context: CallbackContext) -> None:
    file_id = update.message.document.file_id
    new_file = context.bot.get_file(file_id)
    new_file.download('nome_do_arquivo')
    m.upload('nome_do_arquivo')
    update.message.reply_text('Arquivo salvo com sucesso na sua nuvem Mega!')
    update.message.reply_text('Upload do arquivo concluído!')

def error_handler(update: Update, context: CallbackContext) -> None:
    logger.error(msg="Exceção durante o update", exc_info=context.error)

def main() -> None:
    # Adicione os manejadores no dispatcher
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.document, document_handler))
    dispatcher.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

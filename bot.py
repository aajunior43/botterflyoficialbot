import random
from PIL import Image, ImageDraw, ImageFont
from telegram import Update, Bot
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater, ConversationHandler

TOKEN = '6139212717:AAEFn37NwYuKIS8BXotVNXHVYzG4L9FOSWA'

WATERMARK, COLOR, CORNER = range(3)

def start(update: Update, context: Bot):
    update.message.reply_text('Por favor, envie o texto para a marca d\'água.')
    return WATERMARK

def watermark(update: Update, context: Bot):
    text = update.message.text
    context.user_data['watermark'] = text
    update.message.reply_text('Por favor, escolha a cor para a marca d\'água.')
    return COLOR

def color(update: Update, context: Bot):
    color = update.message.text
    context.user_data['color'] = color
    update.message.reply_text('Por favor, escolha o canto para a marca d\'água (sup_esq, sup_dir, inf_esq, inf_dir).')
    return CORNER

def corner(update: Update, context: Bot):
    corner = update.message.text
    context.user_data['corner'] = corner
    update.message.reply_text('Agora, por favor, envie a imagem que você quer adicionar a marca d\'água.')
    return ConversationHandler.END

def handle_image(update: Update, context: Bot):
    file = context.bot.getFile(update.message.photo[-1].file_id)

    img = Image.open(file.download_as_bytearray())
    width, height = img.size
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('arial.ttf', 30)

    text = context.user_data['watermark']
    color = context.user_data['color']
    corner = context.user_data['corner']

    textwidth, textheight = draw.textsize(text, font)

    if corner == "sup_esq":
        position = (0, 0)
    elif corner == "sup_dir":
        position = (width-textwidth, 0)
    elif corner == "inf_esq":
        position = (0, height-textheight)
    elif corner == "inf_dir":
        position = (width-textwidth, height-textheight)
    else:
        update.message.reply_text('Canto inválido. Use sup_esq, sup_dir, inf_esq, or inf_dir.')
        return

    draw.text(position, text, font=font, fill=color)
    
    img.save('out.png', 'PNG')

    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('out.png', 'rb'))

def main():
    updater = Updater(token=TOKEN, use_context=True)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            WATERMARK: [MessageHandler(Filters.text & ~Filters.command, watermark)],
            COLOR: [MessageHandler(Filters.text & ~Filters.command, color)],
            CORNER: [MessageHandler(Filters.text & ~Filters.command, corner)],
        },
        fallbacks=[MessageHandler(Filters.photo, handle_image)],
    )
    dp.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()

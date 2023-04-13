from os import getenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


app = ApplicationBuilder().token(getenv('TELEGRAM_TOKEN')).build()


def main():    
    app.add_handler(CommandHandler("hello", hello))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
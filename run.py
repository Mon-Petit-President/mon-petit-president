from os import getenv
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from functools import wraps

def admin_only(func):
    @wraps(func)
    def wrapper(update, context, *args, **kwargs):
        # Si l'utilisateur n'est pas un administrateur, envoyer un message d'erreur
        if update.effective_user.id != getenv('TG_ADMIN'):
            return update.message.reply_text(update.effective_user.id)
        
        # Si l'utilisateur est un administrateur, exécuter la fonction
        return func(update, context, *args, **kwargs)
    
    return wrapper

# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")

@admin_only
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text("Ton ID est : "+str(update.effective_chat.id))


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(getenv('TELEGRAM_TOKEN')).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_webhook(
        listen='0.0.0.0',
        port=8080,
        webhook_url=getenv('WEBHOOK_URL')
    )


if __name__ == "__main__":
    main()

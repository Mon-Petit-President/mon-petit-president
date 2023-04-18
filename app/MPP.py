#!/usr/bin/env python
# pylint: import-error
# This program is dedicated to the public domain under the CC0 license.

from os import getenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from app.bot.menus import MainMenuHandler, BetMenuHandler, ChoiceMenuHandler, welcome_menu
from dotenv import load_dotenv

load_dotenv() # Charge les variables d'environnement depuis le fichier .env

############################# Handlers #########################################

def app() -> None :
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(getenv("TELEGRAM_BOT_TOKEN")).build()

    handlers = [
        CommandHandler('start', welcome_menu),
        MessageHandler(filters.TEXT & ~ filters.Regex(r'▶|➡'), MainMenuHandler),
        MessageHandler(filters.TEXT & filters.Regex(r'▶'), BetMenuHandler),
        MessageHandler(filters.TEXT & filters.Regex(r'➡'), ChoiceMenuHandler)
    ]

    for handler in handlers :
        application.add_handler(handler)

    return application
#!/usr/bin/env python
# pylint: import-error
# This program is dedicated to the public domain under the CC0 license.

from os import getenv
from functools import wraps
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import CallbackContext


async def send_telegram(text: str, reply_markup: InlineKeyboardMarkup, update: Update, context: CallbackContext) -> None:
    # Envoi du message au chat_id spécifié avec le texte et le reply_markup fournis
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_markup=reply_markup,
        parse_mode='MarkdownV2'
    )


def admin_only(func):
    @wraps(func)
    def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
        # Si l'utilisateur n'est pas un administrateur, envoyer un message d'erreur
        if int(update.effective_user.id) != int(getenv('TG_ADMIN')):
            return update.message.reply_text("Sorry Dave, I can't do that")
        
        # Si l'utilisateur est un administrateur, exécuter la fonction
        return func(update, context, *args, **kwargs)
    
    return wrapper




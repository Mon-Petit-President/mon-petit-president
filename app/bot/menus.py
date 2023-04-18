#!/usr/bin/env python
# pylint: import-error
# This program is dedicated to the public domain under the CC0 license.

from os import getenv
from functools import wraps
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ContextTypes
from app.bot.keyboards import main_menu_kb, active_bets_kb, user_bets_kb, bet_choices_kb
from app.models.bets import end_bet
from app.bot.utils import admin_only, send_telegram


@admin_only
async def welcome_menu(update: Update, context: CallbackContext) -> None:
    # Envoi du message de bienvenue personnalisé avec le clavier principal
    await send_telegram(
        update=update,
        context=context,
        text=f"Salut {update.message['from']['first_name']}",
        reply_markup=main_menu_kb()
    )


@admin_only
async def MainMenuHandler(update: Update, context : CallbackContext) -> None:
    try:
        if update.message.text == 'Terminer pari':
            reply_text = 'Quel pari ?'
            reply_kb = active_bets_kb()

        elif update.message.text == 'Envoyer Notification':
            reply_text = "Texte de la notification :"
            reply_kb = user_bets_kb(update.effective_chat.id)

        elif update.message.text == 'Retour au menu':
            reply_text = "Les paris en cours :"
            reply_kb = main_menu_kb()

        else:
            reply_text = 'Option inconnue'
            reply_kb = main_menu_kb()
    except Exception:
        reply_text = 'Option inconnue'
        reply_kb = active_bets_kb()

    finally:
        await send_telegram(
            update=update,
            context=context,
            text=reply_text,
            reply_markup=reply_kb,
        )

@admin_only
async def BetMenuHandler(update: Update, context : CallbackContext) -> None:
    try:
        bet_id, _ = update.message.text.split(r'▶ ')
        reply_text = f'Quel est le vainqueur du paris {bet_id} ?'
        reply_kb = bet_choices_kb(bet_id)
    except Exception:
        reply_text = 'Pari inconnu'
        reply_kb = active_bets_kb()
    finally:
        await send_telegram(
            update=update,
            context=context,
            text=reply_text,
            reply_markup=reply_kb,
        )

@admin_only
async def ChoiceMenuHandler(update: Update, context : CallbackContext):
    try:
        bet_id, bc_id, _ = update.message.text.split(r' ➡ ')
        end_bet(bet_id, bc_id)
        reply_text = "Cool bro"
        reply_kb = bet_done_kb()

    except Exception:
        reply_text = 'Option inconnue'
        reply_kb = active_bets_kb()
    finally:
        await send_telegram(
            update=update,
            context=context,
            text=reply_text,
            reply_markup=reply_kb,
        )

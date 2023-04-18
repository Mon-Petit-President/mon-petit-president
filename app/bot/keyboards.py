#!/usr/bin/env python
# pylint: import-error
# This program is dedicated to the public domain under the CC0 license.

from telegram import KeyboardButton, ReplyKeyboardMarkup
from app.models.bets import get_actives_bets, get_bet_choices

############################### Decorators ############################################

def main_menu_button(function):
    """ Décorateur qui prend en entrée une fonction qui renvoie une liste de InlineKeyboardButton
        Puis y ajoute un Callback pour un "allez vers menu"
        Enfin, renvoie le tout prêt à publier grâce au ReplyKeyboardMarkup
    """
    def new_function(*args, **kwargs)-> ReplyKeyboardMarkup:
        ret = function(*args, **kwargs)
        ret.append([KeyboardButton(text='Retour au menu')])
        return ReplyKeyboardMarkup(keyboard=ret, resize_keyboard=True, one_time_keyboard=True)
    return new_function

############################### Keyboards ############################################
@main_menu_button
def keyboard_builder(items : list) -> list:
    return [[KeyboardButton(option)] for option in items]

def main_menu_kb():
    """ Keyboard de Menu Principal """
    return keyboard_builder(['Terminer pari','Envoyer Notification'])

@main_menu_button
def active_bets_kb():
    """ Keyboard de liste de paris"""
    return [[KeyboardButton(f"{bet_id} ▶ {option}")] for bet_id, option in get_actives_bets()]

@main_menu_button
def bet_choices_kb(bet_id):
    """ Keyboard de choix """
    return [[KeyboardButton(f'{bet_id} ➡ {bc_id} ➡ {choice}')]
        for bet_id, bc_id, choice in get_bet_choices(bet_id)]

@main_menu_button
def bet_done_kb():
    return []

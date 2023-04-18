from os import getenv
import requests
from datetime import datetime
from app.utils.utils import handle_errors, send_notification
from app.database.db import put_bet_update, get_collection_id, get_items_from_collection

@handle_errors
def get_actives_bets():
    bets = get_items_from_collection(get_collection_id('Bets'))
    return [(item['id'], item['Question']) for item in bets if item['Active'] or not item['Terminé']]

@handle_errors
def get_bet_choices(bet_id):
    bet_choices = get_items_from_collection(get_collection_id('Bet Choices'))
    return [(int(item['Bet'][0]), int(item['id']), item['Option'])
        for item in bet_choices if int(item['Bet'][0])==int(bet_id)]

@handle_errors
def get_users_bet_choices(bet_id):
    bet_choices = get_items_from_collection(get_collection_id('User Bet Choice'))
    return [
        {   'id' : item['id'],
            'Bet': int(item['Bet'][0]),
            'User': int(item['User'][0]),
            'Bet Choice' : int(item['Bet Choice'][0])
        } for item in bet_choices if int(item['Bet'][0])==int(bet_id)]

@handle_errors
def get_bet_details(bet_id):
    bets = get_items_from_collection(get_collection_id('Bets'), bet_id)
    return [(int(item['Bet'][0]), int(item['id']), item['Option'])
        for item in bet_choices if int(item['Bet'][0])==int(bet_id)]

@handle_errors
def get_info_from_id(user_ids):
    """
    Cette fonction permet d'obtenir les informations (ID, email, nom d'utilisateur) des utilisateurs à partir de leur ID.

    Args:
        user_ids (list): Une liste d'IDs d'utilisateurs.

    Returns:
        list: Une liste de tuples contenant les informations des utilisateurs.
    """

    # Vérification que user_ids est une liste
    if isinstance(user_ids, int):
        user_ids = [user_ids]

    # Récupération des informations des utilisateurs
    try:
        users = [get_items_from_collection(collection_id=get_collection_id('Users'), element=user) for user in user_ids]
    except Exception as e:
        print(f'Failed to get user info: {e}')
        return []

    # Récupération des informations pertinentes pour chaque utilisateur
    return [{
            'id': user['id'],
            'Email' : user['Email'],
            'Username' : user['Username']
        } for user in users if user]


@handle_errors
def end_bet(bet_id, bet_choice_id_winner):
    # Update Bet Collection
    collection_id = get_collection_id(collection_name='Bets')
    payload = {'Terminé': True,'endDate': datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')}
    put_bet_update(payload=payload, collection_id=collection_id,element_id=bet_id)

    # Update Bet Choice Collection
    collection_id = get_collection_id(collection_name='Bet Choices')
    payload = {'Winner': True}
    put_bet_update(payload=payload, collection_id=collection_id,element_id=bet_choice_id_winner)

    participations = get_users_bet_choices(bet_id)

    for participation in participations:
        additional_info = get_info_from_id(participation['User'])[0]
        email = additional_info['Email']
        prenom = additional_info['Username']

        if participation['Bet Choice'] == int(bet_choice_id_winner):
            send_notification(email=email,title_text=f"Pari gagné! Bien joué {prenom}", body_text='10 points pour Grifondor')
        else:
            send_notification(email=email,title_text=f"Pas grave {prenom}, la prochaine fois", body_text='Pari échoué sur le fil')

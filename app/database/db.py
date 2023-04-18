#!/usr/bin/env python
# pylint: import-error
# This program is dedicated to the public domain under the CC0 license.

from os import getenv
import requests
from datetime import datetime
from app.utils.utils import handle_errors, send_notification
from dotenv import load_dotenv

load_dotenv() # Charge les variables d'environnement depuis le fichier .env

ROOT_URL = getenv('ROOT_URL')
MOBILE_BEARER_TOKEN = getenv('MOBILE_BEARER_TOKEN')
HEADERS = {'Authorization': f'{MOBILE_BEARER_TOKEN}','Content-Type': 'application/json'}

@handle_errors
def get_collection_id(collection_name: str) -> str:
    collections_id_map = {
        'Bets': getenv('BETS_TABLE_ID'),
        'Bet Choices': getenv('BET_CHOICES_TABLE_ID'),
        'User Bet Choice': getenv('USER_BET_CHOICE_ID'),
        'Users': getenv('USER_TABLE_ID')
    }
    collection_id = collections_id_map.get(collection_name)
    if not collection_id:
        raise ValueError(f'Unknown collection name: {collection_name}')
    return collection_id

@handle_errors
def get_items_from_collection(collection_id: str, element=None) -> list:
    """
    Cette fonction permet d'obtenir tous les items d'une collection.

    Args:
        collection_id (str): L'ID de la collection.

    Returns:
        list: Une liste de dictionnaires représentant les items.
    """

    # Set up the API request parameters
    url = f'{ROOT_URL}{collection_id}'
    if element:
        url = url+'/'+str(element)
    params = {'offset': 0}

    # Make the API request
    items = []
    while True:
        try:
            response = requests.get(url, headers=HEADERS, params=params)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f'Failed to get items: {e}')
            return None
        
        # Process the API response
        data = response.json()
        if element:
            return data
        items += data['records']
        if len(data['records']) >= 100:
            params['offset'] += 100
        else:
            break

    return items

@handle_errors
def put_bet_update(payload: dict, collection_id: str, element_id: int) -> int:
    url = f'{ROOT_URL}{collection_id}/{element_id}'
    try:
        response = requests.put(url, headers=HEADERS, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f'Impossible d\'update l\'élément à la collection : {e}')
        return 1

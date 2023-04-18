#!/usr/bin/env python
# pylint: import-error
# This program is dedicated to the public domain under the CC0 license.

from os import getenv
import logging
import requests
from dotenv import load_dotenv
from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes

load_dotenv() # Charge les variables d'environnement depuis le fichier .env

MOBILE_APP_ID = getenv('MOBILE_APP_ID')
MOBILE_BEARER_TOKEN = getenv('MOBILE_BEARER_TOKEN')
HEADERS = {'Authorization': f'{MOBILE_BEARER_TOKEN}','Content-Type': 'application/json'}

# Configurer le logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def handle_errors(func):
    """
    Cette fonction est un décorateur qui gère les erreurs levées par une autre fonction.
    Elle logue les erreurs et les relève pour que la fonction appelante les gère.

    Args:
        func (callable): La fonction à décorer.

    Returns:
        callable: La fonction décorée.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.exception(e)
            raise

    return wrapper

def send_notification(email: str, title_text: str, body_text: str) -> int:
    """Send a notification to a user identified by their email.
    
    Args:
        email (str): The email of the user to notify.
        title_text (str): The title of the notification.
        body_text (str): The body of the notification.
        
    Returns:
        int: A status code indicating the outcome of the request:
            - 0: Notification sent successfully
            - 1: Failed to send notification
            - 2: User has revoked permission for push notifications
            - 3: User does not have app installed on their device
    """
    
    # Set up the request payload
    payload = {
        'appId': MOBILE_APP_ID,
        'audience': {'email': email},
        'notification': {
            'titleText': title_text,
            'bodyText': body_text
        }
    }

    # Make the API request
    try: 
        response = requests.post(getenv('NOTIF_URL'), headers=HEADERS, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f'Failed to send notification to {email}: {e}')
        return 1

    # Process the API response
    data = response.json()
    successful_count = data.get('successful', 0)
    failed_count = data.get('failed', 0)
    if successful_count > 0:
        return 0
    elif failed_count > 0:
        print(f'{email} has revoked permission for push notifications')
        return 2
    else:
        print(f'{email} does not have app installed on their device')
        return 3

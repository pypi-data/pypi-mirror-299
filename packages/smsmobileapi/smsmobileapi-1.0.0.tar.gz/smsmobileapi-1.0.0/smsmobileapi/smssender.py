# smsmobileapi/smssender.py

import requests

class SMSSender:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url_send = "https://api.smsmobile.com/sendsms"  # Remplace par l'URL d'envoi
        self.api_url_received = "https://api.smsmobile.com/getsms"  # Remplace par l'URL pour lire les SMS reçus

    def send_message(self, to, message):
        payload = {
            'apikey': self.api_key,
            'recipients': to,
            'message': message
        }
        
        try:
            response = requests.post(self.api_url_send, data=payload)
            response.raise_for_status()
            return response.json()  # Retourne la réponse de l'API en JSON
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def get_received_messages(self):
        payload = {
            'apikey': self.api_key
        }
        
        try:
            response = requests.get(self.api_url_received, params=payload)
            response.raise_for_status()
            return response.json()  # Retourne la liste des SMS reçus
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

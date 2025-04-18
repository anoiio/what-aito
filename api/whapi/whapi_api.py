import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from a .env file


def send_whapi_request(endpoint, params=None, method='POST'):
    headers = {
        'Authorization': f"Bearer {os.getenv('TOKEN')}"
    }
    url = f"{os.getenv('API_URL')}/{endpoint}"
    if params:
        if 'media' in params:
            details = params.pop('media').split(';')
            with open(details[0], 'rb') as file:
                m = MultipartEncoder(fields={**params, 'media': (details[0], file, details[1])})
                headers['Content-Type'] = m.content_type
                response = requests.request(method, url, data=m, headers=headers)
        elif method == 'GET':
            response = requests.get(url, params=params, headers=headers)
        else:
            headers['Content-Type'] = 'application/json'
            response = requests.request(method, url, json=params, headers=headers)
    else:
        response = requests.request(method, url, headers=headers)
    print('Whapi response:', response.json())
    return response.json()


def set_hook():
    if os.getenv('BOT_URL'):
        settings = {
            'webhooks': [
                {
                    'url': os.getenv('BOT_URL'),
                    'events': [
                        {'type': "messages", 'method': "post"}
                    ],
                    'mode': "method"
                }
            ]
        }
        send_whapi_request('settings', settings, 'PATCH')


def get_channel_messages(chat_id, count, time_from, time_to, from_me=False):
    endpoint = f"messages/list/{chat_id}"
    params = f"count={count}&time_from={time_from}&time_to={time_to}&from_me={str(from_me).lower()}&normal_types=true"
    response = send_whapi_request(endpoint, params, method='GET')
    return response['messages']

def get_channel_messages_count(chat_id, count, from_me=False):
    endpoint = f"messages/list/{chat_id}"
    params = f"count={count}&from_me={str(from_me).lower()}&normal_types=true"
    response = send_whapi_request(endpoint, params, method='GET')
    return response['messages']

def send_message(chat_id, text):
    endpoint = '/messages/text'
    params = {
          "to": chat_id,
          "body": text
    }
    response = send_whapi_request(endpoint, params, method='POST')
    print(response)

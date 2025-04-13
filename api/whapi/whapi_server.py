from flask import Flask, request
import os
from dotenv import load_dotenv

from api.whapi.whapi_api import send_whapi_request

load_dotenv()  # Load environment variables from a .env file

app = Flask(__name__)


@app.route('/hook/messages', methods=['POST'])
def handle_new_messages():
    try:
        messages = request.json.get('messages', [])
        endpoint = None
        for message in messages:
            sender = {'to': message.get('chat_id')}
            sender['body'] = "Hi there!"
            endpoint = 'messages/text'

        if endpoint is None:
            return 'Ok', 200
        response = send_whapi_request(endpoint, sender)
        print(f"Response from Whapi: {response}")
        return 'Ok', 200

    except Exception as e:
        print(e)
        return str(e), 500


@app.route('/', methods=['GET'])
def index():
    return 'Bot is running'


if __name__ == '__main__':
    # set_hook()
    port = os.getenv('PORT') or (443 if os.getenv('BOT_URL', '').startswith('https:') else 80)
    app.run(port=port, debug=True)

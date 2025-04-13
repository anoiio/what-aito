from api.whapi.whapi_api import get_channel_messages
from api.whapi.whapi_api import send_message
from datetime import datetime, timedelta
from api.openAI.openAI_api import OpenAIClient
import csv
from io import StringIO


def summarize_chat(chat_id, time_from, time_to, prompt, model, max_output_tokens):
    messages = get_channel_messages(chat_id, 499, time_from, time_to)

    if not messages:
        return 'no updates'
    print(messages)
    messages_csv = extract_text_messages_csv(messages)
    response = summarize_messages(messages_csv, prompt, model, max_output_tokens)

    if response['status'] == 'failed':
        print(response['error'])
        return None

    summary = response['summary']
    return summary


def format_message(source_chat_name, summ):
    return f"{source_chat_name}: \n {summ}"


def summarize_and_send(summarize_chat_id, source_chat_name, send_chat_id, period_in_hours, prompt, model, max_output_tokens):
    time_to = datetime.now()
    time_from = time_to - timedelta(hours=period_in_hours)

    summ = summarize_chat(summarize_chat_id, int(time_from.timestamp()), int(time_to.timestamp()), prompt, model, max_output_tokens)
    message = format_message(source_chat_name, summ)
    send_message(send_chat_id, message)
    print(summ)

def extract_text(message):
    if message.get('type') == 'text':
        return message.get('text', {}).get('body')
    elif message.get('type') == 'image':
        return message.get('image', {}).get('caption')
    elif message.get('type') == 'video':
        return message.get('video', {}).get('caption')
    elif message.get('type') == 'document':
        return message.get('document', {}).get('caption')
    elif message.get('type') == 'link_preview':
        return message.get('link_preview', {}).get('body')
    return None

def extract_text_messages_json(messages):
    processed_messages = []
    for message in messages:
        text_body = extract_text(message)
        if text_body:
            processed_message = {
                'ts': message.get('timestamp'),  # Short for timestamp
                'from': message.get('from'),  # Short for 'from'
                'text': text_body  # Text body
            }
            processed_messages.append(processed_message)
    return processed_messages


def extract_text_messages_csv(messages):
    processed_messages = extract_text_messages_json(messages)

    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=['ts', 'from', 'text'])
    writer.writeheader()
    writer.writerows(processed_messages)
    csv_content = output.getvalue()
    output.close()
    return csv_content


def summarize_messages(messages, prompt, model, max_output_tokens):
    openai_client = OpenAIClient()
    response = openai_client.get_response(prompt, messages, model, max_output_tokens)
    if response.error is not None:
        return {
            'status' : "failed",
            'error' : response.error
        }
    return {
        'status': "success",
        'summary': response.output[0].content[0].text
    }

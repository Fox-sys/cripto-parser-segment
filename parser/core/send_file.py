import requests


def send_file(title, bot_token, chat_id, content: str):
    requests.post(
        f'https://api.telegram.org/bot{bot_token}/sendDocument?chat_id={chat_id}&caption={title}',
        files={'document': content.encode()})


def send_new(bot_token, chat_id, content):
    params = {
        'chat_id': chat_id,
        'text': content,
        'disable_web_page_preview': True
    }
    requests.get('https://api.telegram.org/bot' + bot_token + '/sendMessage', params=params)
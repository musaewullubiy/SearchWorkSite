# pip install googletrans==3.1.0a0
from googletrans import Translator
from flask import Flask, request
import logging
import json

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

sessionStorage = {}


def get_translate(word):
    translator = Translator()
    output = translator.translate(word, dest='en', src='ru')
    return output.text


@app.route('/post', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)

    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(response, request.json)

    logging.info('Request: %r', response)

    return json.dumps(response)


def handle_dialog(res, req):
    if req['session']['new']:
        res['response']['text'] = \
            'Привет! Я умею переводить слова, если хочешь перевод, скажи "Переведи слово: <слово>"!'
        return
    if req['request']['original_utterance'].lower().startswith('переведи слово:'):
        dest = get_translate(req['request']['original_utterance'][15:])
        res['response']['text'] = dest
    else:
        res['response']['text'] = 'Не поняла, скажите "Переведи слово: <слово>", чтобы я его вам перевела'


if __name__ == '__main__':
    app.run()

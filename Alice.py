from flask import Flask, request
import logging
import requests

import json

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

session = {}
sessionStorage = {}


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

    handle_dialog(request.json, response)

    logging.info('Response: %r', request.json)

    return json.dumps(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']
    sessionStorage[user_id] = {
        'suggests': [
            "Мои задачи",
            "Посмотреть задачу",
            "Просроченные задачи",
            "Хочу добавить задачу",
            "Делегировать задачу",
            "Поставить дедлайн задачи",
            "Утановить таймер на задачу"
        ]
    }
    if req['session']['new']:
        res['response']['text'] = 'Привет! Введите свой логин и пароль для авторизации в формате: login:password'
        return
    if session == {}:
        try:
            login, password = req['request']['original_utterance'].split(':')
            answer = requests.get('')
            if requests.get(''):
                session['user_id'] = ''
                session['username'] = login
                session['token'] = ''
                res['response']['text'] = 'Вы авторизированы! Что вы хотите сделать?'
                res['response']['buttons'] = get_suggests(session['user_id'])
        except Exception:
            res['response']['text'] = 'Неверные данные, введите корректные'
            return

    for command in req['session']['command']:
        if command == 'Мои задачи':
            pass
        if command == 'Посмотреть задачу':
            pass
        if command == 'Просроченные задачи':
            pass
        if command == 'Хочу добавить задачу':
            pass
        if command == 'Делегировать задачу':
            pass
        if command == 'Поставить дедлайн задачи':
            pass
        if command == 'Установать задчу':
            pass


def get_suggests(user_id):
    session = sessionStorage[user_id]

    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests']
    ]

    session['suggests'] = session['suggests']
    sessionStorage[user_id] = session
    return suggests


if __name__ == '__main__':
    app.run()

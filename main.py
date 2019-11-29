import requests
import time
import logging
import os

import telebot

token = os.environ['TOKEN']
chat = int(os.environ['CHART_ID'])
host = os.environ['HOST']
auth = os.environ['AUTH']

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s: %(funcName)s - %(levelname)s - %(message)s',
    filename='logs.log'
)

logger = logging.getLogger(__name__)

bot = telebot.TeleBot(token)

while True:
    try:
        response = requests.get(
            host,
            headers={
                'Authorization': auth
            }
        )
        data = response.json()

        for key, item in data.items():
            if not item['status']:
                bot.send_message(
                    chat,
                    ('Проблема с {} на продакшен сервере Узбат\n'
                    'Детали: {}').format(
                        key,
                        item['error']
                    )
                )

    except Exception as e:
        logger.exception(e)
        bot.send_message(
            chat,
            'Не смог проверить состояние продакшен сервера Узбат'
        )

    time.sleep(30*60)
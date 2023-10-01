import requests
from dotenv import load_dotenv
import os
from telegram.ext import Updater, CommandHandler
from telegram import Bot

load_dotenv()
# Replace 'YOUR_BOT_TOKEN' with the actual token you received from BotFather
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv('CHAT_ID')


def send_telegram_message(mess):
    # The message that will be sent
    message = mess

    # setting up the url
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"

    # send it
    try:
        requests.get(url)
        print("message sent")
    except:
        print("message failed to sent")



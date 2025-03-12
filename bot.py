import requests
import time
import telebot
from bs4 import BeautifulSoup

# Твой токен бота
import os
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные из .env

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = telebot.TeleBot(TOKEN)

URL = "https://kolejka.gdansk.uw.gov.pl/branch/5"  # Сайт, который нужно мониторить

def check_availability():
    """Проверяет сайт на наличие свободных дат"""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        if "Brak wolnych terminów" not in soup.text:
            message = "⚠️ Появились свободные даты! Проверь сайт: " + URL
            bot.send_message(CHAT_ID, message)
            print("✅ Сообщение отправлено!")
        else:
            print("❌ Свободных дат нет.")
    else:
        print(f"Ошибка {response.status_code}: не удалось загрузить страницу.")

# Запуск проверки каждую минуту
if __name__ == "__main__":
    while True:
        check_availability()
        time.sleep(60)  # Проверять раз в минуту

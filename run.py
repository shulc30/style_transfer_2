from bot.bot import bot, dp
from bot.handlers import *
import logging

# Логирование
logging.basicConfig(level=logging.INFO, filename="logs/bot.log", filemode="w", format="%(asctime)s - %(message)s")

if __name__ == "__main__":
    print("Бот запущен!")
    dp.run_polling(bot)

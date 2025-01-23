import torch
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# Конфигурация бота
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Токен теперь берется из переменных окружения
MODEL_PATH = r"C:\Users\Администратор\Desktop\style_transfer_bot\models\G_AB.pth"
INPUT_DIR = "uploads/input"
OUTPUT_DIR = "uploads/output"

# Определяем устройство
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

try:
    model_state = torch.load("models/G_AB.pth", map_location="cpu")
    print("Файл успешно загружен")
except Exception as e:
    print(f"Ошибка загрузки: {e}")


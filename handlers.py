import os
from aiogram import types
from aiogram.filters import Command
from bot.bot import bot, dp
from bot.model import process_image
from bot.config import INPUT_DIR, OUTPUT_DIR

# Команда /start
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.reply("Привет! Отправьте мне изображение, и я преобразую его в стиль Клода Моне!")

# Обработка изображений
@dp.message(lambda message: message.photo)
async def handle_photo(message: types.Message):
    try:
        # Получаем самое качественное фото из списка
        photo = message.photo[-1]

        # Указываем пути для входного и выходного изображений
        input_path = os.path.join(INPUT_DIR, f"{message.from_user.id}_input.jpg")
        output_path = os.path.join(OUTPUT_DIR, f"{message.from_user.id}_output.jpg")

        # Убедимся, что папки для входных и выходных файлов существуют
        os.makedirs(INPUT_DIR, exist_ok=True)
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        # Скачиваем файл от пользователя
        file_info = await bot.get_file(photo.file_id)
        await bot.download_file(file_info.file_path, input_path)
        print(f"Изображение пользователя сохранено: {input_path}")

        # Обрабатываем изображение
        stylized_image = await process_image(input_path)
        if stylized_image is None:
            raise ValueError("Не удалось стилизовать изображение: process_image вернула None")

        # Сохраняем стилизованное изображение
        stylized_image.save(output_path)
        print(f"Стилизованное изображение сохранено: {output_path}")

        # Отправляем стилизованное изображение обратно пользователю
        with open(output_path, 'rb') as photo_file:
            await message.reply_photo(photo=types.BufferedInputFile(photo_file.read(), filename="stylized.jpg"), caption="Ваше изображение в стиле Клода Моне!")

        # Удаляем временные файлы
        os.remove(input_path)
        os.remove(output_path)
        print("Временные файлы удалены.")
    except Exception as e:
        print(f"Ошибка при обработке изображения: {e}")
        await message.reply("Произошла ошибка при обработке изображения. Попробуйте снова.")











import os

# Создание необходимых папок
def create_folders(paths):
    for path in paths:
        os.makedirs(path, exist_ok=True)

# Пример использования
create_folders(["uploads/input", "uploads/output", "logs"])

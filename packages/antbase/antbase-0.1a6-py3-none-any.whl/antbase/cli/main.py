'''Консольная команда antbase'''

import sys, os
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, folder_path) # Добавляем этот путь в начало sys.path

from antbase.base import db

print("Hello, ants!\nI'm antbase.cli.main!")
print("\n")  # Проверка значений переменных окружения
for key in os.environ:
    print(f"{key}: {os.environ[key]}")
print("\n")
print("\n")
for path in sys.path: print(path)
print("\n")
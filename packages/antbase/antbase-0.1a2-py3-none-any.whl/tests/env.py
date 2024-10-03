import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


# Проверка значений переменных окружения
print("\n")
for key in os.environ:
    print(f"{key}: {os.environ[key]}")
print("\n")

print("\n")
for path in sys.path: print(path)
print("\n")
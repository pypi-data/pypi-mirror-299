from setuptools import setup, find_packages

setup(
    name="antbase",                               # Название пакета
    version="0.1a1",                              # Версия пакета
    packages=find_packages(),                     # Автоматическое нахождение всех пакетов и модулей
    include_package_data=True,                    # Включает дополнительные файлы, указанные в MANIFEST.in
    install_requires=[
        "requests",                               # Зависимости пакета
    ],
    entry_points={
        "console_scripts": [
            "ant=ant.cli:main",                   # Опционально: консольная команда
        ],
    },
    author                        = "Dmitrii Galkin",
    author_email                  = "dg@jart.co",
    description                   = "Antbase package",                     # Краткое описание
    long_description              = open('README.md').read(),
    long_description_content_type = "text/markdown",
    url                           = "https://github.com/antdg/antbase",    # Ссылка на репозиторий
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',                     # Минимальная версия Python
)
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from antbase import Auth, Log

class Tg:
    BOT_NAME      = 'antbase'
    BOT_USERNAME  = 'antbase_bot'
    __bot, _dp    = Auth.get_tg_bot()

    @staticmethod
    def setup_handlers():
        Log.info(f"Telegram bot {Tg.BOT_NAME} got token.")

        # Регистрация обработчиков команд и текстовых сообщений
        Tg.__dp.message.register(Tg.start,  Command(commands=['start']))
        Tg.__dp.message.register(Tg.help,   Command(commands=['help']))
        Tg.__dp.message.register(Tg.stop,   Command(commands=['stop']))
        Tg.__dp.message.register(Tg.create, Command(commands=['create']))
        Tg.__dp.message.register(Tg.echo)

    @staticmethod
    async def start(message: types.Message):
        await message.reply('Hello, ants!')
        Log.info(f"Telegram bot {Tg.BOT_NAME} has been started by {message.from_user.username}")

    @staticmethod
    async def stop(message: types.Message):
        await message.reply('Останавливаемся...')
        Log.info(f"Telegram bot {Tg.BOT_NAME} has been stopped by {message.from_user.username}")

        await Tg.__dp.stop_polling()     # Остановка polling
        await Tg.__bot.session.close()   # Закрываем сессию бота
        loop = asyncio.get_event_loop()  # Завершаем события
        loop.stop()

    @staticmethod
    async def help(message: types.Message):
        await message.reply('Сам! Всё сам!')

    @staticmethod
    async def create(message: types.Message):
        await message.reply('Сам! Всё сам!')

    @staticmethod
    async def echo(message: types.Message):
        await message.reply(f'Птица Говорун.\nОтличается редким умом и сообразительностью.\n\n{message.text}')

    @staticmethod
    async def main():
        # Настраиваем обработчики
        Tg.setup_handlers()

        # Запуск polling
        await Tg.__dp.start_polling(Tg.__bot)

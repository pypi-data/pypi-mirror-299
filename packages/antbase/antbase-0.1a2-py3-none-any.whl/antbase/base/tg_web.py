import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from fastapi import FastAPI, Request

from antbase import Auth, Log

class Tg:
    BOT_NAME      = 'antbase'
    BOT_USERNAME  = 'antbase_bot'
    __bot, __dp   = Auth.get_tg_bot()

    # URL вебхука и параметры сервера
    WEBHOOK_HOST = 'https://your-domain.com'  # Замените на ваш домен
    WEBHOOK_PATH = '/webhook'  # Путь для получения вебхуков
    WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

    # FastAPI-приложение
    app = FastAPI()

    @staticmethod
    def setup_handlers():
        Log.info(f"Telegram bot {Tg.BOT_NAME} got token.")

        # Регистрация обработчиков команд и текстовых сообщений
        Tg.__dp.message.register(Tg.start, Command(commands=['start']))
        Tg.__dp.message.register(Tg.help, Command(commands=['help']))
        Tg.__dp.message.register(Tg.stop, Command(commands=['stop']))
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
    @Tg.app.on_event("startup")
    async def on_startup():
        # Устанавливаем вебхук при старте приложения
        await Tg.__bot.set_webhook(Tg.WEBHOOK_URL)
        Tg.setup_handlers()

    @staticmethod
    @Tg.app.on_event("shutdown")
    async def on_shutdown():
        # Удаляем вебхук при остановке приложения
        await Tg.__bot.delete_webhook()

    # Конечная точка для получения обновлений от Telegram (вебхуки)
    @Tg.app.post(WEBHOOK_PATH)
    async def process_webhook(request: Request):
        try:
            update = await request.json()
            update_obj = types.Update(**update)
            Dispatcher.set_current(Tg.__dp)  # Устанавливаем текущий диспетчер
            Bot.set_current(Tg.__bot)  # Устанавливаем текущий бот
            await Tg.__dp.process_update(update_obj)  # Обработка обновления
        except Exception as e:
            Log.error(f"Ошибка обработки вебхука: {e}")
        return {"status": "ok"}

# Запуск приложения через Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(Tg.app, host="0.0.0.0", port=8000)

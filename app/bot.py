import os
import sys

import asyncio
import logging

from app.handlers.handlers import router

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from app.scheduler.setup import setup_scheduler

from aiogram.types import BotCommand, BotCommandScopeDefault
from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from app.routes.routes import heleket_order_handler

load_dotenv()
TOKEN = os.getenv("TG_TOKEN")
HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))
WEBHOOK_PATH = '/'
BASE_URL = os.getenv("BASE_URL")

dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


# Функция для установки командного меню для бота
async def set_commands():
    # Создаем список команд, которые будут доступны пользователям
    commands = [BotCommand(command='start', description='Старт')]
    # Устанавливаем эти команды как дефолтные для всех пользователей
    await bot.set_my_commands(commands, BotCommandScopeDefault())


# Функция, которая будет вызвана при запуске бота
async def on_startup() -> None:
    # Устанавливаем командное меню
    await set_commands()
    scheduler = setup_scheduler()
    scheduler.start()
    # Устанавливаем вебхук для приема сообщений через заданный URL
    await bot.set_webhook(BASE_URL)
    logging.info("Бот запущен !")


# Функция, которая будет вызвана при остановке бота
async def on_shutdown() -> None:
    logging.info("Бот остановлен !")
    # Удаляем вебхук и, при необходимости, очищаем ожидающие обновления
    await bot.delete_webhook(drop_pending_updates=True)
    # Закрываем сессию бота, освобождая ресурсы
    await bot.session.close()


# Основная функция, которая запускает приложение
def main() -> None:
    # Подключаем маршрутизатор (роутер) для обработки сообщений
    dp.include_router(router)
    # Регистрируем функцию, которая будет вызвана при старте бота
    dp.startup.register(on_startup)
    # Регистрируем функцию, которая будет вызвана при остановке бота
    dp.shutdown.register(on_shutdown)

    # Создаем веб-приложение на базе aiohttp
    app = web.Application()
    app["bot"] = bot
    app.router.add_post("/demo-post/", heleket_order_handler)

    # Настраиваем обработчик запросов для работы с вебхуком
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,  # Передаем диспетчер
        bot=bot  # Передаем объект бота
    )
    # Регистрируем обработчик запросов на определенном пути
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)

    # Настраиваем приложение и связываем его с диспетчером и ботом
    setup_application(app, dp, bot=bot)

    # Запускаем веб-сервер на указанном хосте и порте
    web.run_app(app, host=HOST, port=PORT)


# Точка входа в программу
if __name__ == "__main__":
    # Настраиваем логирование (информация, предупреждения, ошибки) и выводим их в консоль
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)  # Создаем логгер для использования в других частях программы
    main()  # Запускаем основную функцию


# # ПОЛЛИНГ
# async def main() -> None:
#     bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
#     scheduler = setup_scheduler()
#     scheduler.start()
#     await dp.start_polling(bot)

# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO, stream=sys.stdout)
#     asyncio.run(main())

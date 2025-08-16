import os
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import requests

# Загрузка переменных окружения
load_dotenv()

# Инициализация логгера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Конфигурация API погоды
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
CITY = 'Moscow'
WEATHER_URL = f'http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={WEATHER_API_KEY}&units=metric&lang=ru'

# Инициализация бота и диспетчера
bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
dp = Dispatcher()


# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}!\n"
        "Я бот, который показывает текущую погоду в Москве.\n"
        "Используй /help для списка команд."
    )


# Обработчик команды /help
@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = """
📋 Доступные команды:
/start - Начать работу с ботом
/help - Показать это сообщение
/weather - Показать текущую погоду в Москве
"""
    await message.answer(help_text)


# Обработчик команды /weather
@dp.message(Command("weather"))
async def cmd_weather(message: types.Message):
    try:
        response = requests.get(WEATHER_URL)
        data = response.json()

        if response.status_code == 200:
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            description = data['weather'][0]['description']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']

            weather_text = (
                f"🌦 Погода в Москве:\n\n"
                f"🌡 Температура: {temp:.1f}°C (ощущается как {feels_like:.1f}°C)\n"
                f"☁️ Состояние: {description}\n"
                f"💧 Влажность: {humidity}%\n"
                f"🌬 Ветер: {wind_speed} м/с"
            )
            await message.answer(weather_text)
        else:
            await message.answer("Не удалось получить данные о погоде. Попробуйте позже.")
    except Exception as e:
        logger.error(f"Ошибка при запросе погоды: {e}")
        await message.answer("Произошла ошибка при получении данных о погоде.")


# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
import math
import datetime
import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token='6167775436:AAF0o4xvZ2_QidIOuSt6gPqkjUoYGceY1j0')
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    """
    Функция ответа на команду /start
    """
    await message.reply('Привет! Напиши мне название города и я пришлю тебе сводку погоды :)')


@dp.message_handler()
async def get_weather(message: types.Message):
    """
    Функция обработки входных данных.
    """
    try:
        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&lang="
                                f"ru&units=metric&APPID=e004a8822c0603c5df17cc5debbe0203")
        data = response.json()

        city = data['name']
        cur_temp = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        day_length = sunset_timestamp - sunrise_timestamp

        code_to_smile = {
            "Clear": "Ясно \U00002600",
            "Clouds": "Облачно \U00002601",
            "Rain": "Дождь \U00002614",
            "Drizzle": "Дождь \U00002614",
            "Thunderstorm": "Гроза \U000026A1",
            "Snow": "Снег \U0001F328",
            "Mist": "Туман \U0001F32B"
        }

        weather_description = data['weather'][0]['main']
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = 'Посмотри в окно, я не понимаю, что там за погода...'

        await message.reply(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}\n'
                            f'Погода в городе: {city}\n'
                            f'Температура: {round(cur_temp, 1)}°C    {wd}\n'
                            f'Влажность: {humidity}%\n'
                            f'Давление: {math.ceil(pressure/1.333)} мм.рт.ст\n'
                            f'Ветер: {wind} м/с\n'
                            f'Восход солнца: {sunrise_timestamp}\n'
                            f'Закат солнца: {sunset_timestamp}\n'
                            f'Продолжительность дня: {day_length}\n'
                            f'\nХорошего дня!')
    except:
        await message.reply('Ошибка. Проверьте правильность ввода названия города.')


if __name__ == '__main__':
    executor.start_polling(dp)


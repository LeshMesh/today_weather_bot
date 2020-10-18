import telebot
from pyowm import OWM
from pyowm.commons.exceptions import NotFoundError
from pyowm.utils.config import get_default_config

config_dict = get_default_config()
config_dict['language'] = 'ru'

owm = OWM('d491912f4c590c59b48e8f977324a8e2', config_dict)
mgr = owm.weather_manager()

bot = telebot.TeleBot("1300476980:AAGuSoqgZJ9OO8T9M-DXsnlreVEF15sHRwo", parse_mode=None)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Я показываю погоду в твоем городе. Просто отправь мне его название.")


@bot.message_handler(content_types=['text'])
def send_weather(message):
    try:
        observation = mgr.weather_at_place(message.text)
        w = observation.weather
        temp_now = w.temperature("celsius")['temp']
        temp_day = w.temperature("celsius")['temp_max']
        temp_night = w.temperature("celsius")['temp_min']
        wind_now_speed = w.wind()['speed']
        wind_now_deg = w.wind()['deg']
        if 337.6 < wind_now_deg < 22.5:
            wind_now_deg = f'северный'
        elif 22.6 < wind_now_deg < 67.5:
            wind_now_deg = f'северо-восточный'
        elif 67.6 < wind_now_deg < 112.5:
            wind_now_deg = f'восточный'
        elif 112.6 < wind_now_deg < 157.5:
            wind_now_deg = f'юго-восточный'
        elif 157.6 < wind_now_deg < 202.5:
            wind_now_deg = f'южный'
        elif 202.6 < wind_now_deg < 247.5:
            wind_now_deg = f'юго-западный'
        elif 247.6 < wind_now_deg < 292.5:
            wind_now_deg = f'западный'
        else:
            wind_now_deg = f'северо-завадный'

        answer = (
            f'В городе {message.text} сейчас {w.detailed_status}. ' '\n'
            f'Температура {temp_now}. ' '\n'
            f'Ветер {wind_now_deg} {wind_now_speed} м/с'
        )

        bot.send_message(message.chat.id, answer)
    except NotFoundError:
        answer = f'Не могу найти такой город.'
        bot.send_message(message.chat.id, answer)


bot.polling(none_stop=True)

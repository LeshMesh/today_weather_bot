import telebot

from pyowm import OWM
from pyowm.utils.config import get_default_config
config_dict = get_default_config()
config_dict['language'] = 'ru'

owm = OWM('d491912f4c590c59b48e8f977324a8e2', config_dict)
mgr = owm.weather_manager()


bot = telebot.TeleBot("1300476980:AAFDvFUvRlIrGgzVA7EHLAekp25twhdQrc4", parse_mode=None)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")
	
@bot.message_handler(content_types=['text'])
def echo_all(message):

    observation = mgr.weather_at_place(message.text)
    
    w = observation.weather
    temp_now = w.temperature("celsius")['temp']
    temp_day = w.temperature("celsius")['temp_max']
    temp_night = w.temperature("celsius")['temp_min']
    
    wind_now_speed = w.wind()['speed']
    wind_now_deg = w.wind()['deg']
    if wind_now_deg > 337.6 and wind_now_deg < 22.5:
        wind_now_deg = f'северный'
    elif wind_now_deg > 22.6 and wind_now_deg < 67.5:
        wind_now_deg = f'северо-восточный'
    elif wind_now_deg > 67.6 and wind_now_deg < 112.5:
        wind_now_deg = f'восточный'
    elif wind_now_deg > 112.6 and wind_now_deg < 157.5:
        wind_now_deg = f'юго-восточный'
    elif wind_now_deg > 157.6 and wind_now_deg < 202.5:
        wind_now_deg = f'южный'
    elif wind_now_deg > 202.6 and wind_now_deg < 247.5:
        wind_now_deg = f'юго-западный'
    elif wind_now_deg > 247.6 and wind_now_deg < 292.5:
        wind_now_deg = f'западный'
    else:
        wind_now_deg = f'северо-завадный'
    
    answer = (
        f'В городе {message.text} сейчас {w.detailed_status}. ' '\n'
        f'Температура {temp_now}. Днем будет {temp_day}°C, ночью - {temp_night}°C.' '\n'
        f'Ветер {wind_now_deg} {wind_now_speed} м/с'
    )
        
    
    bot.send_message(message.chat.id, answer)
    
bot.polling(none_stop = True)

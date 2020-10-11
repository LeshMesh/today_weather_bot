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
    
    answer = (
        f'В городе {message.text} сейчас {w.detailed_status}. ' '\n'
        f'Температура {temp_now}. '
    )
        
    
    bot.send_message(message.chat.id, answer)
    
bot.polling(none_stop = True)

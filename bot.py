import telebot
from config import *
from logic import * 
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Привет, я бот для генерации фото!
отправь мне текст с запросом и я сделаю по нему фото""")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    promt= message.text
    user_id= message.from_user.id
    path= f"images/{user_id}.png"

    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', API_KEY, SECRET_KEY)
    model_id = api.get_model()
    uuid = api.generate(promt, model_id)
    images = api.check_generation(uuid)
    api.converter_to_png(images[0], path)

    with open(path, 'rb') as img:
        bot.send_photo(message.chat.id, img, caption=f'картинка по запросу:\n {promt}')



bot.infinity_polling()
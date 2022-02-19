import telebot
from telebot import types

token = "5290480699:AAHwcol1GNBlCplq1G8Pk2GbUXZiB4fxS98"
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("Погода", "Расписание", "Дата и время")
    keyboard.row("/Git", "/LMS", "/help")
    bot.send_message(message.chat.id, 'Привет! Хочешь узнать Всё что я умею?\nНажми или напиши команду /help',
                     reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, 'Я умею пытаться')


@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text.lower() == "хочу":
        bot.send_message(message.chat.id, 'Тогда тебе сюда – https://mtuci.ru/')


bot.infinity_polling()
import telebot
import requests
import datetime
from telebot import types

token = "5290480699:AAHwcol1GNBlCplq1G8Pk2GbUXZiB4fxS98"
bot = telebot.TeleBot(token)

city = "Moscow,RU"
appid = "e7156c1332925cb924348b28a2880f42"


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("Погода", "Расписание", "Дата и время")
    keyboard.row("/Git", "/LMS", "/help")
    bot.send_message(message.chat.id, 'Привет! Хочешь узнать Всё что я умею?\nНажми или напиши команду /help',
                     reply_markup=keyboard)


@bot.message_handler(commands=['Git'])
def start_message(message):
    bot.send_message(message.chat.id, 'Ссылка на Репозиторий Бота –\nhttps://github.com/jwizus/Zimin_Bot')


@bot.message_handler(commands=['LMS'])
def start_message(message):
    bot.send_message(message.chat.id, 'Ссылка на LMS –\nhttps://lms.mtuci.ru/lms/my')


@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id,
                     '''
Я обладаю расширенным набором команд и продолжаю учиться каждый день!
Вот что я уже умею делать:
                     
Отвечать на сообщения:
    1)Погода – Точные данные о погоде, включая:
     Погодные условия, Температуру, Миниманильную температуру, Максимальную температуру.
    2)Расписание – постоянно меняющееся расписание занятий.
    3)Дата и Время – Точные дата (день недели) и время.
Отвечать на команды:
    1)Git – Ссылка на репозиторий с Кодом бота.
    2)LMS – Ссылка на вход в электронный университет.
    3)help – Информация о всех возможностях бота.''')


@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text.lower() == "погода":
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                           params={'q': city, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        bot.send_message(message.chat.id, f'''
Город – {city}
Погодные условия – {data['weather'][0]['description']}
Температура: {data['main']['temp']}
Минимальная температура: {data['main']['temp_min']}
Максимальная температура: {data['main']['temp_max']}''')

    if message.text.lower() == "расписание":
        bot.send_message(message.chat.id, 'Как всегда, ждут изменения –\nhttps://mtuci.ru/time-table/')


    if message.text.lower() == "дата и время":
        now = datetime.datetime.now()
        bot.send_message(message.chat.id, f'''
Дата: {now.strftime('%A, %B the %dth, %Y')}
Время: {now.strftime('%H:%M:%S')}''')


bot.infinity_polling()

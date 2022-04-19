import json
import random
import telebot
import requests
from telebot import types
from datetime import datetime, date, timedelta

token = "5290480699:AAHwcol1GNBlCplq1G8Pk2GbUXZiB4fxS98"
bot = telebot.TeleBot(token)

city = "Moscow,RU"
appid = "e7156c1332925cb924348b28a2880f42"
usercities = {}
f = open("/home/ivan/MyApp/assets/even.json", mode="r")
even = json.load(f)
f.close()
f = open("/home/ivan/MyApp/assets/odd.json", mode="r")
odd = json.load(f)
f.close()
week = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота"]

def get_default_markup():
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("Погода", "Расписание", "Дата и время")
    keyboard.row("/Git", "/LMS", "/help")
    keyboard.row("Прогноз на неделю", "Неделя", "JSON")
    return keyboard


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Хочешь узнать Всё что я умею?\nНажми или напиши команду /help',
                     reply_markup=get_default_markup())


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


def get_weather(message):
    if message.text != ".":
        usercities[message.chat.id] = message.text
    city = usercities[message.chat.id]
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                           params={'q': city, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        bot.send_message(message.chat.id, f'''
        Город – {city}
        Погодные условия – {data['weather'][0]['description']}
        Температура: {data['main']['temp']}
        Минимальная температура: {data['main']['temp_min']}
        Максимальная температура: {data['main']['temp_max']}
        Скорость ветра: {data['wind']['speed']}
        Видимость:  {data['visibility']}''')

    except KeyError:
        bot.send_message(message.chat.id, "Город не найден", reply_markup=get_default_markup())


def get_week_weather(message):
    if message.text != ".":
        usercities[message.chat.id] = message.text
    keyboard = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton("Каждые 24 часа")
    btn2 = types.KeyboardButton("Каждые 3 часа")
    keyboard.add(btn1, btn2)
    bot.send_message(message.chat.id, 'Выбери период',
                     reply_markup=keyboard)

    def get_week_weather_period(message):
        try:
            city = usercities.get(message.chat.id)
            period = [int(s) for s in message.text.split() if s.isdigit()][0]
            res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                               params={'q': city, 'units': 'metric', 'lang': 'ru', 'APPID': appid})

            minperiod = 3

            data = res.json()
            for idx, i in enumerate(data['list']):
                if idx % (period / minperiod) == 0:
                    print(f"Дата – {datetime.fromtimestamp(i['dt'])}")
                    bot.send_message(message.chat.id, f'''
                Дата – {datetime.fromtimestamp(i["dt"])}
                Город – {city}
                Погодные условия – {i['weather'][0]['description']}
                Температура: {i['main']['temp']}
                Минимальная температура: {i['main']['temp_min']}
                Максимальная температура: {i['main']['temp_max']}
                Скорость ветра: {i['wind']['speed']}
                Видимость:  {i['visibility']}''', reply_markup=get_default_markup())
        except KeyError:
            bot.send_message(message.chat.id, "Город не найден", reply_markup=get_default_markup())

    bot.register_next_step_handler(message, get_week_weather_period)


@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text.lower() == "погода":
        bot.send_message(message.chat.id, "Какой город?")
        bot.register_next_step_handler(message, get_weather)

    elif message.text.lower() == "расписание":
        learnday = date(2021, 9, 1)
        now = datetime.now().date()
        monday1 = (learnday - timedelta(days=learnday.weekday()))
        monday2 = (now - timedelta(days=now.weekday()))
        weeknum = int(abs((monday2 - monday1).days) / 7) + 1
        current_day_str = None
        if weeknum % 2:
            current_day = odd[f"{now.weekday()}"]
            current_day_str = "Верхняя\n\n"
            for lesson in current_day:
                current_day_str += f"{lesson['time']}\t{lesson['text']}\t{lesson['place']}\n"
            current_day_str=current_day_str[:-1]
        else:
            current_day = even[f"{now.weekday()}"]
            current_day_str = "Нижняя\n\n"
            for lesson in current_day:
                current_day_str += f"{lesson['time']}\t{lesson['text']}\t{lesson['place']}\n"
            current_day_str = current_day_str[:-1]

        bot.send_message(message.chat.id, current_day_str)

    elif message.text.lower() == "неделя":
        learnday = date(2021, 9, 1)
        now = datetime.now().date()
        monday1 = (learnday - timedelta(days=learnday.weekday()))
        monday2 = (now - timedelta(days=now.weekday()))
        weeknum = int(abs((monday2 - monday1).days) / 7) + 1
        out = "Верхняя\n"
        for day in odd.keys():
            current_day_str = f"\n{week[int(day)-1]}\n"
            for lesson in odd[day]:
                current_day_str += f"{lesson['time']}\t{lesson['text']}\t{lesson['place']}\n"
            out+=f"\n{current_day_str}"

        out += "\nНижняя\n"
        for day in even.keys():
            current_day_str = f"\n{week[int(day)-1]}\n"
            for lesson in even[day]:
                current_day_str += f"{lesson['time']}\t{lesson['text']}\t{lesson['place']}\n"
            out += f"\n{current_day_str}"
        out = out[:-1]
        bot.send_message(message.chat.id, out)

    elif message.text.lower() == "дата и время":
        now = datetime.now()
        bot.send_message(message.chat.id, f'''
Дата: {now.strftime('%A, %B the %dth, %Y')}
Время: {now.strftime('%H:%M:%S')}''')

    elif message.text.lower() == "прогноз на неделю":
        bot.send_message(message.chat.id, "Какой город?")
        bot.register_next_step_handler(message, get_week_weather)

    # elif message.text.lower() == "зачет":
    #     with open("/home/ivan/MyApp/citations", mode="r", encoding="utf-8") as citations:
    #         lines = citations.readlines()
    #         bot.send_message(message.chat.id, lines[random.randint(0, len(lines) - 1)])
    elif message.text.lower() == "json":
        bot.send_message(message.chat.id, """JSON (<b>J</b>avaScript <b>O</b>bject <b>N</b>otation) - иерархический текстовый формат представления данных.
Все данные представляются в виде объектов с именем. Объекты могут содержать в себе следующие типы данных:
  строку.
  число.
  объект (JSON object)
  массив.
  булево.
  null.
В данной работе был использован метод json() класса Response.
response.json() возвращает объект результата запроса в формате JSON (если результат был записан в формате JSON, если нет, то возникает ошибка).

OpenWeather API предоставляет возможность получения данных в форматах HTML и XML помимо JSON.
Для получения данных в другом формате, нужно указать дополнительный параметр "mode" в теле запроса, например <code>"api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}&mode=xml"</code>""",
                         parse_mode="HTML"
                         )
bot.infinity_polling()

import telebot
from telebot import types
bot = telebot.TeleBot("7544054516:AAGL4AF1NfaUF6QzU96-Wqh6IZcMc5zOZFA")
from requests import request
from aurora import AuroraParser

@bot.message_handler(commands=["start"])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("Актуальные параметры"))
    keyboard.add(types.KeyboardButton("Прогноз на три дня"))
    bot.send_message(message.chat.id, "Какие показатели изволите?", reply_markup=keyboard)

@bot.message_handler(content_types=["text"])
def second(message):

    if message.text == "Актуальные параметры":
        parser = AuroraParser(wind_speed=0, const_distance=25000)
        parser.get_source_code()
        parser.driver.quit()
        with open("parameters.txt", "r", encoding="utf-8") as m:
            d = m.read()
            bot.send_message(message.chat.id, text=d)

    if message.text == "Прогноз на три дня":
        t = request("get", "https://services.swpc.noaa.gov/text/3-day-geomag-forecast.txt").text
        with open("days.txt", "w") as x:
            x.write(t)
        with open("days.txt", "r", encoding="utf-8") as n:
            lines = n.readlines()
            selected_lines = lines[15:25]
            bot.send_message(message.chat.id, text="\n".join(selected_lines))

bot.polling(none_stop=True)
import requests
import telebot

with open("token", "r") as file:
    tg_token = file.readline()

tg_bot = telebot.TeleBot(tg_token)
tg_bot.set_my_commands([
    telebot.types.BotCommand("/start", "Активировать бота"),
    telebot.types.BotCommand("/help",
        "Вывести список всех доступных команд")
])

tg_bot.polling(none_stop=True)

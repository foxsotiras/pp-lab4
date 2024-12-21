import requests
import telebot

with open("token", "r") as file:
    tg_token = file.readline()

tg_bot = telebot.TeleBot(tg_token)
tg_bot.set_my_commands([
    telebot.types.BotCommand("/start", "Активировать бота"),
    telebot.types.BotCommand("/help",
        "Вывести список всех доступных команд"),
    telebot.types.BotCommand("/isbn", "Найти книгу по ISBN")
])

@tg_bot.message_handler(commands=["start"])
def main(message):
    tg_bot.send_message(
        message.chat.id,
        f"Спасибо, что зашли в нашу библиотеку!")

@tg_bot.message_handler(commands=["help"])
def help(message):
    tg_bot.send_message(
        message.chat.id,
        (f"Список доступных команд:\n\n"
        f"/start - Активировать бота\n"
        f"/help - Вывести список всех доступных команд\n"
        f"/isbn - Найти книгу по ISBN\n"))

@tg_bot.message_handler(commands=["isbn"])
def help(message):
    try:
        isbn = message.text.split(maxsplit=1)[1]
        data = requests\
            .get(f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data")\
            .json()
        book = data[f"ISBN:{isbn}"]

        tg_bot.send_message(
            message.chat.id,
            (f"Название: {book["title"]}\n"
            f"Авторы: {', '.join([author["name"] for author in book["authors"]])}\n"
            f"Дата публикация: {book["publish_date"]}"))
    except IndexError:
        tg_bot.send_message(
            message.chat.id,
            f"Пожалуйста, введите ISBN желаемой книги.")
    except KeyError:
        tg_bot.send_message(
            message.chat.id,
            f"По этому ISBN ничего не найдено.")

tg_bot.polling(none_stop=True)

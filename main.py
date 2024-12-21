import requests
import telebot

with open("token", "r") as file:
    tg_token = file.readline()

tg_bot = telebot.TeleBot(tg_token)
tg_bot.set_my_commands([
    telebot.types.BotCommand("/start", "Активировать бота"),
    telebot.types.BotCommand("/help",
        "Вывести список всех доступных команд"),
    telebot.types.BotCommand("/isbn", "Найти книгу по ISBN"),
    telebot.types.BotCommand("/find_author", "Найти книги автора"),
    telebot.types.BotCommand("/find_books", "Найти книги по названию")
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
        f"/isbn <ISBN> - Найти книгу по ISBN\n"
        f"/find_author - Найти книги автора\n"
        f"/find_books - Найти книги по названию\n"))

@tg_bot.message_handler(commands=["isbn"])
def help(message):
    try:
        isbn = message.text.split(maxsplit=1)[1]
        data = requests\
            .get(f"https://openlibrary.org/api/books",
            params = {
                "bibkeys": f"ISBN:{isbn}",
                "format": "json",
                "jscmd": "data"
            })\
            .json()
        book = data[f"ISBN:{isbn}"]

        tg_bot.send_message(
            message.chat.id,
            (f"Название: {book["title"]}\n"
            f"Авторы: {', '.join([author["name"] for author in book["authors"]])}\n"
            f"Дата публикация: {book["publish_date"]}"
            f"Рейтинг: {book["publish_date"]}"))
    except IndexError:
        tg_bot.send_message(
            message.chat.id,
            f"Пожалуйста, введите ISBN желаемой книги.")
    except KeyError:
        tg_bot.send_message(
            message.chat.id,
            f"По этому ISBN ничего не найдено.")

@tg_bot.message_handler(commands=["find_author"])
def find_author(message):
    tg_bot.send_message(message.chat.id, "Введите имя автора.")
    tg_bot.register_next_step_handler(message, get_author_books)

def get_author_books(message):
    limit = 20
    author = message.text
    author_parse = "+".join([a for a in author.split()])
    data = requests\
        .get(f"https://openlibrary.org/search.json",
        params = {
            "author": f"{author_parse}",
            "limit": f"{limit}"
        })\
        .json()

    if (int(data["numFound"]) == 0):
        tg_bot.send_message(message.chat.id,
            "Этот автор ничего не написал :(")
        return

    books = [book for book in data["docs"]]
    respond = ""
    for i in range(len(books)):
        respond += f"{i+1}. {books[i]["title"]} {books[i].get("ratings_average", 0)}\n"

    tg_bot.send_message(message.chat.id,
    (f"У автора {author} есть следующие книги:\n\n"
    f"{respond}"))

@tg_bot.message_handler(commands=["find_books"])
def find_books(message):
    tg_bot.send_message(message.chat.id, "Введите ключевые слова.")
    tg_bot.register_next_step_handler(message, get_books)

def get_books(message):
    limit = 20
    title = message.text
    title_parse = "+".join([a for a in title.split()])
    data = requests\
        .get(f"https://openlibrary.org/search.json",
        params = {
            "q": f"{title_parse}",
            "limit": f"{limit}"
        })\
        .json()

    if (int(data["numFound"]) == 0):
        tg_bot.send_message(message.chat.id,
            "Не найдено книг с таким названием :(")
        return

    books = [book for book in data["docs"]]
    respond = ""
    for i in range(len(books)):
        respond += f"{i+1}. {books[i]["title"]} {books[i].get("ratings_average", 0)}\n"

    tg_bot.send_message(message.chat.id,
    (f"Найдены следующие книги:\n\n"
    f"{respond}"))

tg_bot.polling(none_stop=True)

import telebot
from telebot import types
from random import randint
import datetime
from threading import Thread
from time import sleep

bot = telebot.TeleBot("5554649259:AAH-MSZTtQomxxMSZMu0B2ccWEjce-p-dNY")

"""menu = types.InlineKeyboardMarkup(row_width=3)
menu.add(
    types.InlineKeyboardButton(text='Hi!', callback_data='b1'),
    types.InlineKeyboardButton(text='Hello!', callback_data='b2')
)"""


def mark(color):
    if color == "green":
        return "\033[42mLOG\033[0m   "
    elif color == "yellow":
        return "\033[43mLOG\033[0m   "
    elif color == "red":
        return "\033[41mLOG\033[0m   "


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет!')
    print("99")


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        print(mark("green") + "Downloading...", end=" ")
        downloaded_file = bot.download_file(file_info.file_path)
        print("Completed", end=" ")
        src = "C:/Users/rezon/PycharmProjects/kvant/static/img/pics/" + file_info.file_path
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        print("Saved")
    except Exception as e:
        print(e)
        bot.reply_to(message, str(e))

    """
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    print 'file.file_path =', file_info.file_path
    downloaded_file = bot.download_file(file_info.file_path)

    with open("image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)"""


@bot.message_handler(content_types=['text', 'document'])
def handle_docs(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        print(mark("green") + "Downloading...", end=" ")
        downloaded_file = bot.download_file(file_info.file_path)
        print("Completed", end=" ")

        src = "C:/Users/rezon/PycharmProjects/kvant/static/img/pics/" + message.document.file_name
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        print("Saved")
    except Exception as e:
        print(e)
        bot.reply_to(message, str(e))
        # kvant_kpfu_photos
        # Kv4ntBot


if __name__ == "__main__":
    print(mark("yellow") + "Bot online!")
    bot.infinity_polling()

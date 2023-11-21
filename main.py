import datetime
import re
import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import and_f
from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                           InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, BotCommand)
import logging

logging.basicConfig(level=logging.INFO)
# получение токена бота
x = open('Токен.txt', 'r')
c = x.readlines()
TOKEN = c[0][11:]
x.close()

# получение id пользователей
c = open('userid.txt', 'r')
userid = []
for i in c.readlines():
    userid.append(int(i))
c.close()
bot = Bot(token=TOKEN)
dp = Dispatcher()

def filter(message: Message):
    c=True # включение выключение фильтра
    return (message.from_user.id in userid) or not c

import BD  # подключение базы данных
from Bot.StartHelp import *  # ответы на комманды start и help
from Bot.InlineKeyboards import *  # получение инлайн клавиатур
from Bot.GeoTime import *  # получение геопозиции и времени
from Bot.products import *  # Команды с продуктами
from Bot.SetMainMenu import *  # создание меню команд

if __name__ == '__main__':

    dp.startup.register(set_main_menu)
    dp.run_polling(bot)

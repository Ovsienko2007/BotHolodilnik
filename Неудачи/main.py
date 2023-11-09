
import schedule
import datetime
import re
import BD # подключение базы данных

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
# токены
x = open('Токены.txt', 'r')
c=x.readlines()
TOKEN = c[0][11:-1]
x.close()

c = open('chatid.txt', 'r')
chatid=[]
chatid1=5636710751

for i in c.readlines():
    chatid.append(int(i))
print(chatid)

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
def start (message):
    if message.chat.id in chatid:
        #Клавиатура с кнопкой запроса локации
        button_1= KeyboardButton(text="Отправить местоположение", request_location=True)
        button_2 = KeyboardButton(text='Продукты')
        button_3 = KeyboardButton(text='Удаление_продуктов')
        button_4 = KeyboardButton(text='Просроченные_продукты')
        keyboard = ReplyKeyboardMarkup(keyboard=[[button_1],[button_3, button_2],[button_4]])


        bot.send_message(message.chat.id, "Поделись местоположением", reply_markup=keyboard)

"""
#Получаю локацию
@bot.message_handler(content_types=['location'])
def location (message):
    print(message)

    def today():
        day = datetime.date.today().day
        month = datetime.date.today().month
        year = datetime.date.today().year
        if day < 10:
            day = '0' + str(day)
        if month < 10:
            month = '0' + str(month)

        date = str(day) + '.' + str(month) + '.' + str(year)
        BD.new_srok(date)
        print(date)

    schedule.every().day.at("00:00").do(today)
    while True:
        schedule.run_pending()

# удаление продукта
@bot.message_handler(commands=['Удаление_продукта'])
def delite(message):
    if message.chat.id in chatid:
        @bot.callback_query_handler(func=lambda call: True)  # запускается при нажатии на кнопку
        def callback_inline(call):
            if str(call.data)[0]=='-':
                global id1
                global message_id2
                id1 = -int(call.data)

                knopki2 = types.InlineKeyboardMarkup()
                knopki2.add(types.InlineKeyboardButton('Удалить', callback_data='Del'))
                knopki2.add(types.InlineKeyboardButton('Отмена', callback_data='No'))

                bot.delete_message(message.chat.id, message_id)
                msg2 = bot.send_message(chat_id,
                                        f"Вы действительно хотите удалить {BD.prod(id1)[0][1]}".format(from_user),
                                        reply_markup=knopki2)
                message_id2 = msg2.message_id

            elif call.data == 'No':
                bot.delete_message(message.chat.id, message_id2)
                kn()
            elif call.data == 'Del':
                bot.delete_message(message.chat.id, message_id2)
                BD.delite(id1)
                kn()

            # Для просроченных продуктов
            elif call.data=='All':
                for i in BD.products_srock():
                    BD.delite_srok(i[0])
                bot.delete_message(chatid1, message_id)
                bot.send_message(chatid1, "Просроченных продуктов нет")
        # сборка клавиатуры из кнопок
        def kn():
            global chat_id
            global from_user

            print(message)
            from_user = message.from_user
            chat_id = message.chat.id

            c = BD.products()
            if c!=[]:
                knopki = types.InlineKeyboardMarkup()
                for i in c:
                    knopki.add(types.InlineKeyboardButton(f'{i[1]}: {i[2]}', callback_data=-i[0]))
                msg=bot.send_message(message.chat.id, "Выбери продукт которых хочешь удалить".format(message.from_user), reply_markup=knopki)
                global message_id
                message_id = msg.message_id
            else:
                bot.send_message(message.chat.id, "Продуктов нет")
        kn()
# удаление просроченных продуктов
def de():
    c = BD.products_srock()
    if c!=[]:
        knopki = types.InlineKeyboardMarkup()
        knopki.add(types.InlineKeyboardButton("Удалить всё", callback_data="All"))
        ans="Просроченные продукты\n"
        for i in c:
            ans+=f'{i[1]}: {i[2]};\n'

        msg=bot.send_message(chatid1, ans, reply_markup=knopki)
        global message_id
        message_id = msg.message_id
    else:
        bot.send_message(chatid1, "Просроченных продуктов нет")
# вывод просроченных продуктов
@bot.message_handler(commands=['Просроченные_продукты'])
def pr_prods(message):
    de()

date='11.11.2023'

# Продукты
@bot.message_handler(commands=['Продукты'])
def product (message):
    if message.chat.id in chatid:
        if BD.products()!=[]:
            # создание текста для сообщения
            ans='Продукты:\n'
            c=1
            for i in BD.products():
                ans+=f'{c}  {i[1]}: {i[2]};\n'
                c+=1
            # отпрака сообщения
            bot.send_message(message.chat.id, ans)
        else:
            bot.send_message(message.chat.id, "Продуктов нет")
    pass

# Добавление продукта
@bot.message_handler(commands=[''])
def product_new (message):
    if message.chat.id in chatid:
        try:
            # Обработка сообщения
            t=message.text
            srok=re.findall(r'\d\d\.\d\d\.\d{4}',t)
            srok=srok[-1]
            prod = re.sub(r'\d\d\.\d\d\.\d{4}', '', t)
            prod=prod[2:]

            # добавление элемента
            BD.new(prod,srok)
        except:
            bot.send_message(message.chat.id, "Не удалось ввсести продукт")



"""
if __name__ == '__main__':
    dp.run_polling(bot)
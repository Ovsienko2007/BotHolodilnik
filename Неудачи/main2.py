import datetime
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot import types
import BD2
import schedule
import re
import logging

logging.basicConfig(level=logging.INFO)

TOKEN = "6080106986:AAFvTaiqrXCECEnFPRuanKPNaEIWxpQgKU8"
bot=telebot. TeleBot (TOKEN)


@bot.message_handler(commands=['help', 'start'])
async def send_welcome (message):
    global chatid1
    chatid1=message.chat.id
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text="Отправить местоположение", request_location=True))
    keyboard.add(KeyboardButton('/Продукты'))
    keyboard.add(KeyboardButton('/Удаление_продуктов'),KeyboardButton('/Просроченные_продукты'))
    #Клавиатура с кнопкой запроса локации
    bot.send_message(message.chat.id, "Поделись местоположением", reply_markup=keyboard)


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
        BD2.new_srok(date)
        print(date)

    schedule.every().day.at("00:00").do(today)
    while True:
        schedule.run_pending()

# удаление продукта
@bot.message_handler(commands=['Удаление_продукта'])
def delite(message):
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
                                    f"Вы действительно хотите удалить {BD2.prod(id1)[0][1]}".format(from_user),
                                    reply_markup=knopki2)
            message_id2 = msg2.message_id

        elif call.data == 'No':
            bot.delete_message(message.chat.id, message_id2)
            kn()
        elif call.data == 'Del':
            bot.delete_message(message.chat.id, message_id2)
            BD2.delite(id1)
            kn()

        # Для просроченных продуктов
        elif call.data=='All':
            for i in BD2.products_srock():
                BD2.delite_srok(i[0])
            bot.delete_message(message.chat.id, message_id)
            bot.send_message(message.chat.id, "Просроченных продуктов нет")
        # сборка клавиатуры из кнопок
    def kn():
        global chat_id
        global from_user

        print(message)
        from_user = message.from_user
        chat_id = message.chat.id

        c = BD2.products()
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
    c = BD2.products_srock()
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
    if BD2.products()!=[]:
        # создание текста для сообщения
        ans='Продукты:\n'
        c=1
        for i in BD2.products():
            ans+=f'{c}  {i[1]}: {i[2]};\n'
            c+=1
        # отпрака сообщения
        bot.send_message(message.chat.id, ans)
    else:
        bot.send_message(message.chat.id, "Продуктов нет")


# Добавление продукта
@bot.message_handler(commands=[''])
def product_new (message):
    try:
        # Обработка сообщения
        t=message.text
        srok=re.findall(r'\d\d\.\d\d\.\d{4}',t)
        srok=srok[-1]
        prod = re.sub(r'\d\d\.\d\d\.\d{4}', '', t)
        prod=prod[2:]

        # добавление элемента
        BD2.new(prod,srok)
    except:
        bot.send_message(message.chat.id, "Не удалось ввсести продукт")




bot.infinity_polling()
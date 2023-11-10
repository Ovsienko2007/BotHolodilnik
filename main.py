import logging
import schedule
import datetime
import re
import BD # подключение базы данных
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                           InlineKeyboardButton, InlineKeyboardMarkup,CallbackQuery)

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

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start (message):
    if message.chat.id in chatid:
        #Клавиатура с кнопкой запроса локации
        button_1= KeyboardButton(text="Отправить местоположение", request_location = True)
        button_2 = KeyboardButton(text='Продукты')
        button_3 = KeyboardButton(text='Удаление продуктов')
        button_4 = KeyboardButton(text='Просроченные продукты')
        keyboard = ReplyKeyboardMarkup(keyboard=[[button_1],[button_3, button_2],[button_4]])
        await message.answer(text='Чего кошки боятся больше?', reply_markup=keyboard)

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
    
"""




@dp.message(F.text == 'Привет')
async def pr_prods(message: Message):
    if message.chat.id in chatid:
        def srok():
            now = datetime.datetime.now()
            BD.new_srok(now.strftime('%d.%m.%Y'))

        def sroc_nap():
            now = datetime.datetime.now()
            if BD.products_srock()!=[] and int(now.strftime('%H'))>=9:
                message.answer("Появились просроченные продукты!")

        schedule.every().day.at("00.00").do(srok)
        schedule.every(1).hour.do(sroc_nap)
        while True:
            schedule.run_pending()
            await asyncio.sleep(1)



# удаление просроченных продуктов

@dp.callback_query(F.data.in_(['DEL_', 'NO_']))
async def DaNet1(callback: CallbackQuery):
    if F.data == 'DEL_':
        for i in BD.products_srock():
            BD.delite_srok(i[0])
        await callback.message.edit_text(
            text='Нет просроченных продуктов')
    else:
        button = InlineKeyboardButton(
            text='Удалить всё',
            callback_data='ALL')
        knopki = InlineKeyboardMarkup(
            inline_keyboard=[[button]]
        )
        ans = "Просроченные продукты\n"
        for i in c:
            ans += f'{i[1]}: {i[2]};\n'

        await callback.message.edit_text(text=ans, reply_markup=knopki)
    await callback.answer()


@dp.callback_query(F.data.in_(['ALL']))
async def Dell_srok(callback: CallbackQuery):
    button_1 = InlineKeyboardButton(
        text='Удалить',
        callback_data='DEL_')
    button_2 = InlineKeyboardButton(
        text='Отмена',
        callback_data='NO_')
    danet2 = InlineKeyboardMarkup(
        inline_keyboard=[[button_1],
                         [button_2]]
    )

    await callback.message.edit_text(
        text='Вы точно убрали ВСЕ просроченные продукты', reply_markup=danet2)
    await callback.answer()

@dp.message(F.text == 'Просроченные продукты')
async def pr_prods(message: Message):
    c = BD.products_srock()
    if c != []:
        button = InlineKeyboardButton(
            text='Удалить всё',
            callback_data='ALL')
        knopki = InlineKeyboardMarkup(
            inline_keyboard=[[button]]
        )
        a = 1
        ans = '\n<b>__Есть просроченные продукты😞__</b>\n'
        for i in c:
            ans += f'{a})  {i[1]}: {i[2]};\n'
            a += 1


        await message.answer(text=ans, reply_markup=knopki, parse_mode='HTML')
    else:
        await message.answer(text="Просроченных продуктов нет")




# Все продукты
def pr():
    products = []
    for i in BD.products():
        button = InlineKeyboardButton(
            text=f'{i[1]}: {i[2]}',
            callback_data=str(i[0]))
        products.append([button])

    return products


# удаление продукта 2 этап
@dp.callback_query(F.data.in_(['DEL','NO']))
async def DaNet2(callback: CallbackQuery):
    print(callback.data)
    if callback.data=='DEL':
        print(id)
        print(BD.prod(id))
        BD.delite(id)
    else:
        pass
    in_keyboard = InlineKeyboardMarkup(
        inline_keyboard=pr()
    )
    if BD.products()!=[]:
        await callback.message.edit_text(
            text='Выбери продукт которых хочешь удалить',
            reply_markup=in_keyboard)
    else:
        await callback.message.edit_text(
            text='Продуктов нет')
    await callback.answer()

# удаление продукта 1 этап
@dp.callback_query()
async def process_buttons_press(callback: CallbackQuery):
    global id
    id =callback.data

    button_1 = InlineKeyboardButton(
        text='Удалить',
        callback_data='DEL')
    button_2 = InlineKeyboardButton(
        text='Отмена',
        callback_data='NO')
    danet = InlineKeyboardMarkup(
        inline_keyboard=[[button_1],
                         [button_2]]
    )

    await callback.message.edit_text(
        text='Вы действительно хотите удалить',
        reply_markup=danet
    )
    await callback.answer()


# удаление продуктов
@dp.message(F.text == 'Удаление продуктов')
async def process_start_command(message: Message):
    if message.chat.id in chatid:
        # сборка клавиатуры из кнопок
        if pr()!=[]:
            in_keyboard = InlineKeyboardMarkup(
                inline_keyboard=pr()
            )
            await message.answer(
                text='Выбери продукт которых хочешь удалить',
                reply_markup=in_keyboard)
        else:
            await message.answer(
                text='Нет продуктов')



@dp.message(F.text == 'Продукты')
async def product(message: Message):
    if message.chat.id in chatid:
        if BD.products()!=[]:
            # создание текста для сообщения
            ans='<b>____________Продукты🍞_____________</b>\n'
            c=1
            for i in BD.products():
                ans+=f'{c})  {i[1]}: {i[2]};\n'
                c+=1
            if BD.products_srock()!=[]:
                c=1
                ans+='\n<b>__Есть просроченные продукты😞__</b>\n'
                for i in BD.products_srock():
                    ans += f'{c})  {i[1]}: {i[2]};\n'
                    c += 1
            # отпрака сообщения
            await message.answer(text=ans, parse_mode='HTML')
        else:
            await message.answer("Продуктов нет")


@dp.message()
async def product_new (message: Message):
    if message.chat.id in chatid:
        try:
            # Обработка сообщения
            t=message.text
            srok=re.findall(r'\d\d\.\d\d\.\d{4}',t)
            srok=srok[-1]
            prod = re.sub(r'\d\d\.\d\d\.\d{4}', '', t)

            # добавление элемента
            BD.new(prod,srok)
        except:
            await message.answer("Не удалось ввсести продукт")




if __name__ == '__main__':
    dp.run_polling(bot)
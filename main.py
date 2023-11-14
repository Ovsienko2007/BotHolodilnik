import logging
import schedule
import datetime
import re
import BD # подключение базы данных
import asyncio
from aiogram import Bot, Dispatcher, F, types

from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                           InlineKeyboardButton, InlineKeyboardMarkup,CallbackQuery)

# получение токена бота
x = open('Токен.txt', 'r')
c=x.readlines()
TOKEN = c[0][11:]
x.close()

# получение id пользователей
c = open('userid.txt', 'r')
userid=[]
for i in c.readlines():
    userid.append(int(i))
print(userid)
userid1=userid[0] # основной чат
c.close()

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()



def start_filter(message: Message):
    return message.text == '/start' or message.text == '/help'
@dp.message(start_filter)
async def start (message):
    if message.from_user.id in userid:
        #Клавиатура с кнопкой запроса локации
        button_1 = KeyboardButton(text='Продукты')
        button_2 = KeyboardButton(text='Удаление продуктов')
        button_3 = KeyboardButton(text='Просроченные продукты')
        button_4 = KeyboardButton(text='Дом')
        keyboard = ReplyKeyboardMarkup(keyboard=[[button_1],[button_2,button_3],[button_4]])
        await message.answer(text=f'Привет, <b>{message.from_user.first_name}</b>!\n\n'
                                  f'Сейчас я вкратце расскажу о себе\n'
                                  f'Я создан, чтобы напоминать людям о появлении просроченных продуктов.n'
                                  f'Ты вводишь в меня пр',
                             reply_markup=keyboard,
                             parse_mode='HTML')


@dp.message(F.location)
@dp.edited_message(F.location)
async def geo(message: Message):
    if message.from_user.id in userid:
        lat = "%.4f"%float(message.location.latitude)
        long = "%.4f"%float(message.location.longitude)
        BD.geo_update(message.from_user.id, str(long), str(lat))


# создание команды /home
def Home(message: Message):
    return message.text == '/home'

# создание файла с координатами "дома"
@dp.message(Home)
async def home_com(message: Message):
    if message.from_user.id == userid1:
        with open('home.txt', 'a') as f:  # создание файла если его нет
            pass
        with open('home.txt', 'r+') as f:  # внос данных
            c=BD.geo(message.from_user.id)
            f.writelines("\n".join(c))

# получение координат "дома" из файла
def home():
    with open('home.txt', 'r') as f:
        ge = f.readlines()
        ge[0]=ge[0][:-1]
    return list(map(float, ge))

# отправка геопозиции "дома" из файла
@dp.message(F.text=="Дом")
async def home1(message: Message):
    if message.from_user.id in userid:
        ge = home()
        await bot.send_location(chat_id=message.chat.id, latitude=ge[0], longitude=ge[1])


"""@dp.message(F.text == 'Привет')
async def pr_prods(message: Message):
    if message.from_user.id in userid:
        await bot.send_message(chat_id=message.chat.id, text=' sdf')
        def srok():
            now = datetime.datetime.now()
            BD.new_srok(now.strftime('%d.%m.%Y'))
        def geo():
            message.answer("Появились просроченные продукты!")

        async def sroc_nap():
            await bot.send_message(chat_id=message.chat.id, text=' sdf')
            now = datetime.datetime.now()
            print(now.strftime('%H:%M'))
            if BD.products_srock()==[] and int(now.strftime('%H'))>=9:
                await message.answer("Появились просроченные продукты!")

        schedule.every().day.at("00:00").do(srok)
        schedule.every(10).seconds.do(sroc_nap)
        schedule.every(3).seconds.do(geo)

        while True:
            schedule.run_pending()
            await asyncio.sleep(1)"""

def geo123():
    us=list(map(float, BD.geo(userid1)))
    ho=home()
    print(us)
    print(ho)
    if BD.geo(userid1)==('No', 'No'):
        return True
    elif ho[0]-0.0002<us[0]<ho[0]+0.0002 and ho[1]-0.0002<us[1]<ho[1]+0.0002:
        return True
    else:
        return False

def Time(message: Message):
    return message.text == '/time'
@dp.message(Time)
async def ti(message: Message):
    print(geo123())
    flag = True

    while True:
        now = datetime.datetime.now()

        if now.strftime('%H:%M')=="00:00" and flag:
            print(1)
            BD.new_srok(now.strftime('%d.%m.%Y'))
            flag=False

        elif now.strftime('%H:%M')!="00:00":
            flag = True

        async def sroc_nap():
            print(3)
            now = datetime.datetime.now()
            print(now.strftime('%H:%M'))
            if BD.products_srock()==[] and int(now.strftime('%H'))>=9:
                print(4)
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
    if message.from_user.id in userid:
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
    if callback.data=='DEL':
        id=BD.del_prod_id(callback.from_user.id)
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
    BD.del_prod_id_update(callback.from_user.id,callback.data)

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
    if message.from_user.id in userid:
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
    if message.from_user.id in userid:
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


@dp.message(F.text)
async def product_new (message: Message):
    if message.from_user.id in userid:
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

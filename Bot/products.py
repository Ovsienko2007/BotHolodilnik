from main import *

print(3)
# удаление просроченных продуктов
@dp.message(F.text.regexp(r'Просроченные продукты.+'))
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
            ans = '<b>__Есть просроченные продукты😞__</b>\n'
            for i in c:
                ans += f'{a})  {i[1]}: {i[2]};\n'
                a += 1


            await message.answer(text=ans, reply_markup=knopki, parse_mode='HTML')
        else:
            await message.answer(text="Просроченных продуктов нет 👍")

# Все продукты
def pr():
    products = []
    for i in BD.products():
        button = InlineKeyboardButton(
            text=f'{i[1]}: {i[2]}',
            callback_data=str(i[0]))
        products.append([button])

    return products

@dp.message(F.text.regexp(r'Продукты.+'))
async def product(message: Message):
    if message.from_user.id in userid:
        print(3)
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
            await message.answer("Продуктов нет ❌")

# удаление продуктов
@dp.message(F.text.regexp(r'Удаление продуктов.+'))
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
                text='Нет продуктов ❌')

@dp.message(F.text.regexp(r'.+\d\d\.\d\d\.\d{4}'))
async def product_new (message: Message):
    if message.from_user.id in userid:
        # Обработка сообщения
        t=message.text
        srok=re.findall(r'\d\d\.\d\d\.\d{4}',t)
        srok=srok[-1]
        prod = re.sub(r'\d\d\.\d\d\.\d{4}', '', t)
        # добавление элемента
        BD.new(prod,srok)
        await message.answer("Продукт добавлен ✔")
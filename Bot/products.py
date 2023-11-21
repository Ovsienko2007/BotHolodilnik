from main import *

# удаление просроченных продуктов
@dp.message(and_f(F.text.regexp(r'Просроченные продукты 🗑'), filter))
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


def pr2():
    products = []
    for i in BD.products():
        if i[-1]!="0":
            button = InlineKeyboardButton(
            text=f'{i[1]}: {i[2]}',
            callback_data=str(-i[0]))
            products.append([button])

    return products

@dp.message(and_f(F.text.regexp(r'Продукты 🍞'), filter))
async def product(message: Message):
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
@dp.message(and_f(F.text.regexp(r'Удаление продуктов ❌'), filter))
async def process_start_command(message: Message):
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


@dp.message(and_f(F.text.regexp(r'Обновление срока годности 🔄'), filter))
async def process_start_command(message: Message):
    # сборка клавиатуры из кнопок
    if pr()!=[]:
        in_keyboard = InlineKeyboardMarkup(
            inline_keyboard=pr2()
        )
        await message.answer(
            text='Выбери продукт у которого была вскрыта упаковка 🔪',
            reply_markup=in_keyboard)
    else:
        await message.answer(
            text='Продуктов c упаковкой нет ❌')

def sroki1(srok):
    now = datetime.datetime.now()

    d=int(srok[:2])
    m=int(srok[3:5])
    y=int(srok[6:])
    if int(now.strftime('%Y')) < y:
        return True
    elif int(now.strftime('%Y')) == y:
        if int(now.strftime('%m')) < m:
            return True
        elif int(now.strftime('%m')) == m:
            if int(now.strftime('%d')) <= d:
                return True
            else:
                return False
        else:
            return False
    else:
        return False
def sroki2(srok):

    d=int(srok[:2])
    m=int(srok[3:5])
    y=int(srok[6:])
    try:
        date = datetime.datetime(y,m,d)
        return True
    except:
        return False

@dp.message(and_f(F.text.regexp(r'.+\d\d\.\d\d\.\d{4}\s?\d*'), filter))
async def product_new (message: Message):
    # Обработка сообщения
    t=message.text
    a = re.search(r'\d\d\.\d\d\.\d{4}', t)
    srok=re.findall(r'\d\d\.\d\d\.\d{4}',t)
    srok=srok[-1]

    prodsr = re.sub(r'\d\d\.\d\d\.\d{4}', '', t)
    sr=prodsr[a.start()+1:]
    prod=prodsr[:a.start()-1]
    if sroki2(srok):
        if sroki1(srok):
            # добавление элемента
            if sr!="":
                BD.new(prod,srok,int(sr))
            else:
                BD.new(prod, srok)
            await message.answer("Продукт добавлен ✔")
        else:
            await message.answer("Продукт не добавлен ❌\n\n"
                                 "<i>Продукт просрочен\n</i>"
                                 "<i>Проверьте правильно ли введена дата</i>",
                                 parse_mode='HTML')
    else:
        await message.answer("Продукт не добавлен ❌\n\n"
                             "<i>Дата записана не корректно\n</i>"
                             "<i>Проверьте правильно ли введена дата</i>",
                             parse_mode='HTML')
@dp.message(and_f(F.text.regexp(r'.+\d+'), filter))
async def product_new (message: Message):
    # Обработка сообщения
    t=message.text
    print(t)
    srok=re.findall(r'\d+',t)
    srok=srok[-1]
    prod = re.sub(r'\d+', '', t)[:-1]
    await message.answer("Срок годности для продукта добавлен ✔")
    BD.new_prod_srok_2(prod,srok)


def prod_er(message: Message):
    return message.text[0]!="/"

@dp.message(and_f(~F.text.regexp(r'Дом.+'), ~F.location, prod_er, filter))
async def prod_er_ans (message: Message):
    await message.answer("Продукт не добавлен ❌\n\n"
                         "Проверьте соответствие образцу\n"
                         "Образец: \n<i>Продукт 23.12.2023</i>",
                         parse_mode='HTML')
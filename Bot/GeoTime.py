import BD
from main import *

# получение геопозиции
@dp.message(and_f(F.location, filter))
async def geo(message: Message):
    lat = "%.4f"%float(message.location.latitude)
    long = "%.4f"%float(message.location.longitude)
    BD.geo_update(message.from_user.id, str(long), str(lat))
    await message.answer("Геопозиция принята ✔")

# обновление геопозиции
@dp.edited_message(and_f(F.location, filter))
async def geo(message: Message):
    lat = "%.4f"%float(message.location.latitude)
    long = "%.4f"%float(message.location.longitude)
    BD.geo_update(message.from_user.id, str(long), str(lat))

# получение координат "дома" из файла
def home():
    try:
        with open('home.txt', 'r') as f:
            ge = f.readlines()
            ge[0]=ge[0][:-1]
        return list(map(float, ge))
    except:
        return []

# создание команды /home
def Home(message: Message):
    return message.text == '/home'

# создание файла с координатами "дома"
@dp.message(and_f(Home, filter))
async def home_com(message: Message):
    c=BD.geo(message.from_user.id)
    if c!=('No', 'No'):
        with open('home.txt', 'a') as f:  # создание файла если его нет
            pass
        with open('home.txt', 'r+') as f:  # внос данных
            f.writelines("\n".join(c))
        await message.answer('Геопозиция "Дома" установлена ✔')
    else:
        await message.answer('Геопозиция "Дома" не установлена ❌\n\n'
                             '<i>Чтобы установить точку дома надо, прежде скинуть боту геопозицию</i>',
                             parse_mode='HTML')

# отправка геопозиции "дома" из файла
@dp.message(and_f(F.text.regexp(r'Дом 🏠'), filter))
async def home1(message: Message):
    ge = home()
    if ge!=[]:
        await bot.send_location(chat_id=message.chat.id, latitude=ge[0], longitude=ge[1])
    else:
        await message.answer('Точка дома не была установлена 😞\n\n'
                             '<i>Чтобы использовать эту функцию установите точку "Дома"</i>',
                             parse_mode='HTML')

# проверка находится ли пользователь "Дома"
def geo123(user):
    us=BD.geo(user)
    ho=home()
    if BD.geo(user)==('No', 'No'): # Если данные о геопозиции не были переданы
        return True
    elif ho[0]-0.0002<float(us[0])<ho[0]+0.0002 and ho[1]-0.0002<float(us[1])<ho[1]+0.0002: # Если пользователь находится дома
        return True
    else:  # Если пользователь не находится дома
        return False


# создание команды /time
def Time(message: Message):
    return message.text == '/time'
@dp.message(and_f(Time , filter))
async def ti(message: Message):
    # создание переменных флагов
    flag1 = True
    flag2 = True
    # запуск цикла времени
    while True:
        # перенос просроченных продуктов из одной таблицы в другую
        now = datetime.datetime.now()  # получение текущего времени
        BD.new_srok(str((int(now.strftime('%d'))-1))+'.'+now.strftime('%m.%Y'))
        if flag1 and int(now.strftime('%H')) != 0 and message.from_user.id==userid[0]:
            BD.update_prod_srok_2()
            flag1=False

        if BD.products_srock() != [] and int(now.strftime('%H')) >= 9 and int(now.strftime('%H')) <= 21 and flag2\
                and geo123(message.from_user.id) :
            await message.answer('Появились просроченные продукты😞 \n\n'
                                 '<i>Нажмите на кнопку "Просроченные продукты" , чтобы просмотреть их</i>',
                                 parse_mode='HTML')
            flag2=False
        if int(now.strftime('%H')) == 0:
            flag2=True

        await asyncio.sleep(60)
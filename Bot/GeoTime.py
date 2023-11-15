from main import *


@dp.message(F.location)
@dp.edited_message(F.location)
async def geo(message: Message):
    if message.from_user.id in userid:
        lat = "%.4f"%float(message.location.latitude)
        long = "%.4f"%float(message.location.longitude)
        BD.geo_update(message.from_user.id, str(long), str(lat))

# получение координат "дома" из файла
def home():
    with open('home.txt', 'r') as f:
        ge = f.readlines()
        ge[0]=ge[0][:-1]
    return list(map(float, ge))

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

# отправка геопозиции "дома" из файла
@dp.message(F.text=="Дом")
async def home1(message: Message):
    if message.from_user.id in userid:
        ge = home()
        await bot.send_location(chat_id=message.chat.id, latitude=ge[0], longitude=ge[1])

# проверка находится ли пользователь "Дома"
def geo123(user):
    us=list(map(float, BD.geo(user)))
    ho=home()
    if BD.geo(userid1)==('No', 'No'): # Если данные о геопозиции не были переданы
        return True
    elif ho[0]-0.0002<us[0]<ho[0]+0.0002 and ho[1]-0.0002<us[1]<ho[1]+0.0002: # Если пользователь находится дома
        return True
    else:  # Если пользователь не находится дома
        return False


# создание команды /time
def Time(message: Message):
    return message.text == '/time'
@dp.message(Time)
async def ti(message: Message):
    # создание переменных флагов
    flag1 = True
    flag2 = True

    # запуск цикла времени
    while True:
        now = datetime.datetime.now() # получение текущего времени

        if now.strftime('%H:%M')=="00:00" and flag1:
            # Перенос просроченных продуктов из одной таблицы в другую
            BD.new_srok(now.strftime('%d.%m.%Y'))
            flag1=False

        elif now.strftime('%H:%M')!="00:00" and not flag1: # обновление флага
            flag1 = True

        if BD.products_srock() != [] and int(now.strftime('%H')) >= 9 and int(now.strftime('%H')) <= 21 and flag2\
                and geo123(message.from_user.id) :
            await message.answer('Появились просроченные продукты😞 \n\n'
                                 '<i>Нажмите на кнопку "Просроченные продукты" , чтобы просмотреть их</i>',
                                 parse_mode='HTML')
            flag2=False
        elif int(now.strftime('%H')) == 0 and not flag2:
            flag2=True

        await asyncio.sleep(1)

from aiogram import Bot, Dispatcher, types
from BD import new_user

x = open('Токен.txt', 'r')
c=x.readlines()
TOKEN = c[0][11:]
x.close()
bot = Bot(token=TOKEN)
dp = Dispatcher()
with open('userid.txt','a') as f: #создание файла если его нет
    pass
@dp.message()
def start (message: types.Message):
    id = []
    with open('userid.txt', "r") as n:  # чтение всех id
        id += n.readlines()

    #добавление новых id
    c = open('userid.txt', 'a+')
    if f'{str(message.from_user.id)}\n' not in id: # добавление новых id
        c.writelines(f'{str(message.from_user.id)}\n')
    c.close()
    new_user(message.from_user.id)
if __name__ == '__main__':
    dp.run_polling(bot)


from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart

x = open('Токены.txt', 'r')
c=x.readlines()
TOKEN = c[0][11:-1]
x.close()


bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
def start (message):
    c = open('chatid.txt', 'r')
    print(message.chat.id)
    print(type(message.chat.id))
    c.write(f'{message.chat.id}\n')
    c.close()


if __name__ == '__main__':
    dp.run_polling(bot)
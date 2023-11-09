import telebot

x = open('Токены.txt', 'r+')
c=x.readlines()
TOKEN = c[0][11:-1]
bot=telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start (message):
    print(message.chat.id)
    print(type(message.chat.id))
    x.write(f'chatid: {message.chat.id}')
    x.close()



bot.infinity_polling()
from main import *


def start_help(message: Message):
    return message.text == '/start' or message.text == '/help'
@dp.message(and_f(start_help, filter))
async def start (message):
    BD.new_user(message.from_user.id)
    #Клавиатура с кнопкой запроса локации
    button_1 = KeyboardButton(text='Продукты 🍞')
    button_2 = KeyboardButton(text='Удаление продуктов ❌')
    button_3 = KeyboardButton(text='Просроченные продукты 🗑️')
    button_4 = KeyboardButton(text='Дом 🏠')
    keyboard = ReplyKeyboardMarkup(keyboard=[[button_1],[button_2,button_3],[button_4]])
    await message.answer(text=f'Привет, <b>{message.from_user.first_name}</b> 👋!\n\n'
                              f'Сейчас я вкратце расскажу о себе\n'
                              f'Я создан, чтобы напоминать людям о появлении просроченных продуктов.\n'
                              f'Ты вводишь в меня продукты и после их срок годности\n'
                              f'Например <i>Продукт 23.12.2023</i>\n'
                              f'<b>Продукты вводить отдельными сообщениями</b>\n'
                              f'Я их запоминаю и при появлении просроченных продуктов сообщаю тебе об этом\n'
                              f'Кроме того, боту можно скинуть свою геопозицию, чтобы он знал, когда вы дома, и сообщал о появлении просроченнах продуктов\n\n'
                              f'Я могу ответить на следующие сообщения:\n'
                              f'1). Продукты <i>Я вывожу все продукты</i>;\n'
                              f'2). Удаление продуктов <i>Ты можешь удалить один из продуктов</i>;\n'
                              f'3). Указывает точку дома <i>Я укажу, где находится "Дом"</i>;\n'
                              f'4). Просроченные продукты <i>Я вывожу все просроченные продукты</i>;\n\n'
                              f'Имеются также следующие команды:\n'
                              f'/start и /help - выводят это сообщение;\n'
                              f'/time - напоминает о появлении просроченных продуктов;\n'
                              f'/home - устанавливает геолокацию дома;\n\n'
                              f'Некоторые подробности использования команд:\n'
                         ,reply_markup=keyboard,
                         parse_mode='HTML')
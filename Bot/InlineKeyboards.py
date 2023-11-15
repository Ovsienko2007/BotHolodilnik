from main import *
from Bot.products import *

@dp.callback_query(F.data.in_(['DEL_', 'NO_']))
async def DaNet1(callback: CallbackQuery):
    if F.data == 'DEL_':
        for i in BD.products_srock():
            BD.delite_srok(i[0])
        await callback.message.edit_text(
            text='Нет просроченных продуктов 👍')
    else:
        button = InlineKeyboardButton(
            text='Удалить всё',
            callback_data='ALL')
        knopki = InlineKeyboardMarkup(
            inline_keyboard=[[button]]
        )
        ans = '\n<b>__Есть просроченные продукты😞__</b>\n'
        for i in c:
            ans += f'{i[1]}: {i[2]};\n'

        await callback.message.edit_text(text=ans, reply_markup=knopki)
    await callback.answer()


@dp.callback_query(F.data.in_(['ALL']))
async def Dell_srok(callback: CallbackQuery):
    button_1 = InlineKeyboardButton(
        text='✔ Удалить',
        callback_data='DEL_')
    button_2 = InlineKeyboardButton(
        text='❌ Отмена',
        callback_data='NO_')
    danet2 = InlineKeyboardMarkup(
        inline_keyboard=[[button_1],
                         [button_2]]
    )

    await callback.message.edit_text(
        text='Вы точно убрали <b>ВСЕ</b> просроченные продукты?', reply_markup=danet2, parse_mode='HTML')
    await callback.answer()

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
            text='Продуктов нет ❌')
    await callback.answer()

# удаление продукта 1 этап
@dp.callback_query()
async def process_buttons_press(callback: CallbackQuery):
    BD.del_prod_id_update(callback.from_user.id,callback.data)

    button_1 = InlineKeyboardButton(
        text='✔ Удалить',
        callback_data='DEL')
    button_2 = InlineKeyboardButton(
        text='❌ Отмена',
        callback_data='NO')
    danet = InlineKeyboardMarkup(
        inline_keyboard=[[button_1],
                         [button_2]]
    )

    await callback.message.edit_text(
        text=f'Вы действительно хотите удалить <b>{BD.prod(callback.data)[0][1]}</b>',
        reply_markup=danet,
        parse_mode='HTML'
    )
    await callback.answer()

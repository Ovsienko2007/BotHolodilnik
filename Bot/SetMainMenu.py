from main import *

async def set_main_menu(bot: Bot):

    # Создаем список с командами и их описанием для кнопки menu
    main_menu_commands = [
        BotCommand(command='/start',
                   description='Начало работы'),
        BotCommand(command='/help',
                   description='Информация о боте'),
        BotCommand(command='/home',
                   description='Устанавливает точку дома'),
        BotCommand(command='/time',
                   description='Напоминает о появлении просроченных продуктов')
    ]

    await bot.set_my_commands(main_menu_commands)
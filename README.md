# Bot_holodilnik

Бот который сообщает о появлении просроченных продуктов в холодильнике

![Иллюстрация к проекту](https://github.com/Ovsienko2007/Bot_holodilnik/blob/main/pictures/1.jpg)

## Содержание
[Установка](#Ystanovka)

[Технологии](#Tehn)

[Пример](#prim)

[Автор](#avt)


<a name="Ystanovka"><h2>Установка</h2></a>

1). Склонировать репозиторий git clone

2). Создать бота в [BotFather](https://t.me/botfatherи), получить токен

![Иллюстрация к проекту](https://github.com/Ovsienko2007/Bot_holodilnik/blob/main/pictures/2.png)

3). Вставить токен в API_kluchi.txt

4). Запускаем командную строку Линукса. [Скачать здесь](https://gitforwindows.org/)

Пишем команды:

```
python -m venv ./venv
```
 
```
source ./venv/Scripts/activate
```

```
pip install -r requirements.txt
```

5). Запустить программу [chatid](https://github.com/Ovsienko2007/Bot_holodilnik/chatid.py) и отправить боту сообщение
```
\start
```

<a name="Tehn"><h2>Технологии</h2></a>

Python 3.10

PyTelegramBotAPI (TeleBot)

sqlalchemy (библиотека для работы с базами данных)

schedule (библиотека для работы со временем)

<a name="avt"><h2>Автор</h2></a>
Овсиекно Глеб

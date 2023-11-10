# BotHolodilnik

Бот который сообщает о появлении просроченных продуктов в холодильнике

![Иллюстрация к проекту](https://github.com/Ovsienko2007/BotHolodilnik/blob/master/pictures/1.jpg)

## Содержание
[Установка](#Ystanovka)

[Технологии](#Tehn)

[Пример](#prim)

[Автор](#avt)


<a name="Ystanovka"><h2>Установка</h2></a>

1). Склонировать репозиторий git clone

2). Создать бота в [BotFather](https://t.me/botfatherи), получить токен

![Иллюстрация к проекту](https://github.com/Ovsienko2007/BotHolodilnik/blob/master/pictures/2.png)

3). Вставить токен в API_kluchi.txt

4). Создать файлы: 
```
Токены.txt
```
```
chatid.txt
```

5). Написать в командной строке

| Linux                                  | Windows                              |
| -------------------------------------- | ------------------------------------ |
| ```python -m venv ./venv```            | ```python -m venv my-venv```         |
| ```source venv/bin/activate```         | ```venv\Scripts\activate```          |
| ```pip install -r requirements.txt```  | ```pip install -r requirements.txt```|


6). Запустить программу [1.py](https://github.com/Ovsienko2007/BotHolodilnik/blob/master/1.py) и отправить боту сообщение
```
\start
```

7). Запустить программу [BD.py](https://github.com/Ovsienko2007/BotHolodilnik/blob/master/BD.py)

8). Запустить программу [main.py](https://github.com/Ovsienko2007/BotHolodilnik/blob/master/main.py)

<a name="Tehn"><h2>Технологии</h2></a>

Python 3.10

PyTelegramBotAPI (TeleBot)

sqlalchemy (библиотека для работы с базами данных)

schedule (библиотека для работы со временем)

<a name="avt"><h2>Автор</h2></a>
Овсиекно Глеб

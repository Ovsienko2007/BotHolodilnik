import sqlite3


conn = sqlite3.connect('BD.db')
cur = conn.cursor()
#cur.execute("ВАШ-SQL-ЗАПРОС-ЗДЕСЬ;")
cur.execute("""CREATE TABLE IF NOT EXISTS Products(
    product_id    INTEGER NOT NULL,
    product_name  TEXT,
    product_srok  TEXT,
    product_srok2 INTEGER DEFAULT 1,
    Upakovka      TEXT    DEFAULT 1,
    PRIMARY KEY (product_id)
);
""")
cur.execute("""CREATE TABLE IF NOT EXISTS Product_srok(
    product_id   INTEGER NOT NULL,
    product_name TEXT,
    product_srok TEXT,
    PRIMARY KEY (product_id)
    );
""")
cur.execute("""CREATE TABLE IF NOT EXISTS Product_srok2 (
    product_name string UNIQUE,
    product_srok TEXT DEFAULT 1
);
""")
cur.execute("""CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER UNIQUE,
    lat     TEXT DEFAULT No,
    long    TEXT DEFAULT No,
    prod_id_del INTEGER DEFAULT 0
);
""")

conn.commit()
conn.close()

# Вывод продуктов
def products():
    # Устанавливаем соединение с базой данных
    connection = sqlite3.connect('BD.db')
    cursor = connection.cursor()
    # Выбираем всех пользователей
    cursor.execute('SELECT * FROM Products')
    pr = cursor.fetchall()
    # Закрываем соединение
    connection.close()
    return pr

def new_prod_srok_2(prod,srok):
    prod = prod.lower()
    connection = sqlite3.connect('BD.db')
    cursor = connection.cursor()
    # Добавляем нового продукта
    try:
        cursor.execute('INSERT INTO Product_srok2 (product_name, product_srok) VALUES (?, ?)', (prod,srok))
    except:
        cursor.execute('UPDATE Product_srok2 SET product_srok= ? WHERE product_name = ?', (srok, prod))
    # Сохраняем изменения и закрываем соединение
    connection.commit()
    connection.close()

def update_prod_srok_2():
    connection = sqlite3.connect('BD.db')
    cursor = connection.cursor()
    for i in products():
        if i[4]=='0':
            cursor.execute('UPDATE Products SET product_srok2= ? WHERE product_id = ?', (i[3]-1,i[0]))
    connection.commit()
    connection.close()

def del_prod_srok_2(a):
    # Устанавливаем соединение с базой данных
    connection = sqlite3.connect('BD.db')
    cursor = connection.cursor()
    # Меняем значение
    cursor.execute('UPDATE Products SET Upakovka = 0 WHERE product_id = ?', (a,))
    # Сохраняем изменения и закрываем соединение
    connection.commit()
    connection.close()
def prod_srok_2(a):
    a=a.lower()
    # Устанавливаем соединение с базой данных
    connection = sqlite3.connect('BD.db')
    cursor = connection.cursor()
    # Выбираем продукт
    cursor.execute('SELECT * FROM Product_srok2 WHERE product_name = ?', (a,))
    t = cursor.fetchall()
    # Закрываем соединение
    connection.close()
    if t!=[]:
        return t[0][1]
    else:
        return 1

# Добавление элементов
def new(prod,srok,*args):
    # Устанавливаем соединение с базой данных
    connection = sqlite3.connect('BD.db')
    cursor = connection.cursor()
    # Добавляем новый продукт
    if args!=():
        cursor.execute('INSERT INTO Products (product_name, product_srok, product_srok2) VALUES (?, ?, ?)', (prod, srok))

    else:
        sr=0
        for i in prod.split():
            if prod_srok_2(i)!=1:
                sr=prod_srok_2(i)
                break
        cursor.execute('INSERT INTO Products (product_name, product_srok, product_srok2) VALUES (?, ?, ?)', (prod, srok, sr))

    # Сохраняем изменения и закрываем соединение
    connection.commit()
    connection.close()



# удаление продукта
def delite(a):
    # Устанавливаем соединение с базой данных
    connection = sqlite3.connect('BD.db')
    cursor = connection.cursor()
    # Удаляем пользователя "newuser"
    cursor.execute('DELETE FROM Products WHERE product_id = ?', (a,))
    # Сохраняем изменения и закрываем соединение
    connection.commit()
    connection.close()

# Выбор продукта по id
def prod(a):
    # Устанавливаем соединение с базой данных
    connection = sqlite3.connect('BD.db')
    cursor = connection.cursor()
    # Выбираем продукт
    cursor.execute('SELECT * FROM Products WHERE product_id = ?', (a,))
    pr = cursor.fetchall()
    # Закрываем соединение
    connection.close()
    return pr

# Добавление просроченных продуктов
def new_srok(a):
    # Устанавливаем соединение с базой данных
    connection = sqlite3.connect('BD.db')
    cursor = connection.cursor()
    # Выбираем продукт
    cursor.execute('SELECT * FROM Products WHERE product_srok = ?', (a,))
    pr = cursor.fetchall()
    cursor.execute('SELECT * FROM Products WHERE  product_srok2=0')
    pr+=cursor.fetchall()
    for i in pr:
        delite(i[0])
    # Закрываем соединение
    connection.commit()
    connection.close()

    # Устанавливаем соединение с базой данных
    connection = sqlite3.connect('BD.db')
    cursor = connection.cursor()
    # Добавляем просроченные продукты
    for i in pr:
        cursor.execute('INSERT INTO Product_srok (product_name, product_srok) VALUES (?, ?)', (i[1], i[2]))
    # Закрываем соединение
    connection.commit()
    connection.close()

# Вывод всех просроченных продуктов
def products_srock():
    # Устанавливаем соединение с базой данных
    connection = sqlite3.connect('BD.db')
    cursor = connection.cursor()
    # Выбираем все продукты
    cursor.execute('SELECT * FROM Product_srok')
    pr = cursor.fetchall()
    # Закрываем соединение
    connection.close()
    return pr

 # Удаляем просроченного продукта
def delite_srok(a):
    # Устанавливаем соединение с базой данных
    connection = sqlite3.connect('BD.db')
    cursor = connection.cursor()
    # Удаляем продукт
    cursor.execute('DELETE FROM Product_srok WHERE product_id = ?', (a,))
    # Сохраняем изменения и закрываем соединение
    connection.commit()
    connection.close()

# Добавляем нового пользователя
def new_user(a):
    try:
        # Устанавливаем соединение с базой данных
        connection = sqlite3.connect('BD.db')
        cursor = connection.cursor()
        # Добавляем нового пользователя
        cursor.execute('INSERT INTO Users (user_id) VALUES (?)', (a,))
        # Сохраняем изменения и закрываем соединение
        connection.commit()
        connection.close()
    except:
        pass

# Обновление геопозиции пользователя
def geo_update(a, long, lat):
    # Устанавливаем соединение с базой данных
    connection = sqlite3.connect('BD.db')
    cursor = connection.cursor()
    # Обнавляем геопозицию
    cursor.execute('UPDATE Users SET long= ?, lat= ? WHERE user_id = ?', (long, lat, a))
    # Сохраняем изменения и закрываем соединение
    connection.commit()
    connection.close()

# Вывод геопозиции пользователя
def geo(a):
    # Устанавливаем соединение с базой данных
    connection = sqlite3.connect('BD.db')
    cursor = connection.cursor()
    # Выбираем геопозицию пользователя
    cursor.execute('SELECT * FROM Users WHERE user_id = ?', (a,))
    ge = cursor.fetchall()
    # Закрываем соединение
    connection.close()
    return ge[0][1], ge[0][2]

#  Добавление id удаляемого продукта
def del_prod_id_update(a, prod_id):
    # Устанавливаем соединение с базой данных
    connection = sqlite3.connect('BD.db')
    cursor = connection.cursor()
    # Добавляем id удаляемого продукта
    cursor.execute('UPDATE Users SET prod_id_del = ? WHERE user_id = ?', (prod_id, a))
    # Сохраняем изменения и закрываем соединение
    connection.commit()
    connection.close()

# Вывод id удаляемого продукта
def del_prod_id(a):
    # Устанавливаем соединение с базой данных
    connection = sqlite3.connect('BD.db')
    cursor = connection.cursor()
    # Получаем id удаляемого продукта
    cursor.execute('SELECT prod_id_del FROM Users WHERE user_id = ?', (a,))
    pr = cursor.fetchall()
    # Закрываем соединение
    connection.close()
    return pr[0][0]


if __name__ == "__main__":
    del_prod_srok_2(1)
    for i in products():
        print(f'{i[0]}  {i[1]}: {i[2]} | {i[3]};')
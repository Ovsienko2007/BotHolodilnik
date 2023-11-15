import sqlite3


conn = sqlite3.connect('BD.db')
cur = conn.cursor()
#cur.execute("ВАШ-SQL-ЗАПРОС-ЗДЕСЬ;")
cur.execute("""CREATE TABLE IF NOT EXISTS Products(
    product_id   INTEGER NOT NULL,
    product_name TEXT,
    product_srok TEXT,
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
cur.execute("""CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER UNIQUE,
    lat     TEXT DEFAULT No,
    long    TEXT DEFAULT No,
    prod_id_del INTEGER DEFAULT 0
);
""")

conn.commit()
conn.close()

# Добавление элементов
def new(prod,srok):
    # Устанавливаем соединение с базой данных
    connection = sqlite3.connect('BD.db')
    cursor = connection.cursor()
    # Добавляем новый продукт
    cursor.execute('INSERT INTO Products (product_name, product_srok) VALUES (?, ?)', (prod, srok))
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
    for i in products():
        print(f'{i[0]}  {i[1]}: {i[2]};')
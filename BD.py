import sqlite3

conn = sqlite3.connect('products.db')
cur = conn.cursor()
#cur.execute("ВАШ-SQL-ЗАПРОС-ЗДЕСЬ;")
cur.execute("""CREATE TABLE IF NOT EXISTS Products(
    product_id   INTEGER NOT NULL,
    product_name TEXT,
    product_srok TEXT,
    PRIMARY KEY (
        product_id
    )
    );
""")
cur.execute("""CREATE TABLE IF NOT EXISTS Product_srok(
    product_id   INTEGER NOT NULL,
    product_name TEXT,
    product_srok TEXT,
    PRIMARY KEY (
        product_id
    )
    );
""")

conn.commit()
conn.close()

# Добавление элементов
def new(prod,srok):
    # Устанавливаем соединение с базой данных
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()
    # Добавляем новый продукт
    cursor.execute('INSERT INTO Products (product_name, product_srok) VALUES (?, ?)', (prod, srok))
    # Сохраняем изменения и закрываем соединение
    connection.commit()
    connection.close()


# изменение срока годности
def update(a,new):
    # Устанавливаем соединение с базой данных
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()
    # Обновляем срок годности
    cursor.execute('UPDATE Products SET product_srok = ? WHERE product_name = ?', (new, a))
    # Сохраняем изменения и закрываем соединение
    connection.commit()
    connection.close()

# удаление продукта
def delite(a):
    # Устанавливаем соединение с базой данных
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()
    # Удаляем пользователя "newuser"
    cursor.execute('DELETE FROM Products WHERE product_id = ?', (a,))
    # Сохраняем изменения и закрываем соединение
    connection.commit()
    connection.close()

# Вывод продуктов
def products():
    # Устанавливаем соединение с базой данных
    connection = sqlite3.connect('products.db')
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
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()
    # Выбираем продукт
    cursor.execute('SELECT * FROM Products WHERE product_id = ?', (a,))
    pr = cursor.fetchall()
    # Закрываем соединение
    connection.close()
    return pr

# Вывод просроченных продуктов
def new_srok(a):
    # Устанавливаем соединение с базой данных
    connection = sqlite3.connect('products.db')
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
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()
    # Добавляем просроченные продукты
    for i in pr:
        cursor.execute('INSERT INTO Product_srok (product_name, product_srok) VALUES (?, ?)', (i[1], i[2]))
    # Закрываем соединение
    connection.commit()
    connection.close()

def products_srock():
    # Устанавливаем соединение с базой данных
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()
    # Выбираем всех пользователей
    cursor.execute('SELECT * FROM Product_srok')
    pr = cursor.fetchall()
    # Закрываем соединение
    connection.close()
    return pr


def delite_srok(a):
    # Устанавливаем соединение с базой данных
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()
    # Удаляем пользователя "newuser"
    cursor.execute('DELETE FROM Product_srok WHERE product_id = ?', (a,))
    # Сохраняем изменения и закрываем соединение
    connection.commit()
    connection.close()


if __name__ == "__main__":
    for i in products():
        print(f'{i[0]}  {i[1]}: {i[2]};')
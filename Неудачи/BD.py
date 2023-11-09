import sqlalchemy as db


# Создание бд
def bd():
    try:
        global Products
        global conn

        engine = db.create_engine('sqlite:///bd.db')
        conn = engine.connect()
        metadata = db.MetaData()

        Products = db.Table('Products', metadata,
                            db.Column('product_id', db.Integer, primary_key=True),
                            db.Column('product_name', db.Text),
                            db.Column('product_srok', db.Text)
                            )
        metadata.create_all(engine)
    except:
        pass


# Добавление элементов
def new(prod,srok):
    insertion_query = Products.insert().values([
      {'product_name': prod, 'product_srok': srok},
    ])
    conn.execute(insertion_query)
    return


# Вывод просроченных продуктов
def products_srok(a):
    q = db.select([Products]).where(Products.columns.product_srok==a)
    results = conn.execute(q)
    return results

# Вывод продуктов
def products():
    q = db.select([Products])
    results = conn.execute(q)
    return results


# изменение срока годности
def update(a,new):
    update_query = db.update(Products).where(Products.columns.product_id==a).values(product_srok=new)
    conn.execute(update_query)
    return

# Выбор продукта по id
def prod(a):
    q = db.select([Products]).where(Products.columns.product_id == a)
    results = conn.execute(q)
    return results

# удаление продукта
def delite(a):
    delete_query = db.delete(Products).where(Products.columns.product_id ==a)
    conn.execute(delete_query)


# вывод по умолчанию
if __name__ == "__main__":
    bd()
    for i in products():
        print(f'{i[0]}  {i[1]}: {i[2]};')


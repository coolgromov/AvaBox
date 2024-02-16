import sqlite3

# Создание соединения с базой данных
conn = sqlite3.connect('museum.db')

# Создание курсора для выполнения SQL-запросов
cursor = conn.cursor()

# Создание таблицы для хранения предметов коллекции
cursor.execute('''CREATE TABLE IF NOT EXISTS museum_items
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT,
                   description TEXT,
                   author TEXT,
                   year INTEGER)''')

# Пример вставки данных в таблицу
cursor.execute("INSERT INTO museum_items (name, description, author, year) VALUES (?, ?, ?, ?)",
               ('Имя предмета', 'Описание предмета', 'Автор предмета', 2022))

# Подтверждение изменений в базе данных
conn.commit()

# Пример выборки данных из таблицы
cursor.execute("SELECT * FROM museum_items")
rows = cursor.fetchall()
for row in rows:
    print(row)

# Закрытие соединения с базой данных
conn.close()

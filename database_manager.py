import sqlite3


# Подключение к базе данных (или ее создание, если она не существует)
def get_connection():
    return sqlite3.connect('users_database.db')


# Создание таблицы, если она еще не создана
def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            city TEXT,
            age INTEGER,
            descriptions TEXT,
            status TEXT,
            photo TEXT
        )
    ''')
    conn.commit()
    conn.close()


# Добавление нового пользователя в базу данных
def add_user(name, city, age, descriptions, status, photo):
    conn = get_connection()
    cursor = conn.cursor()
    # Вставляем данные пользователя в таблицу
    cursor.execute('''
        INSERT INTO users (name, city, age, descriptions, status, photo)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, city, age, descriptions, status, photo))
    conn.commit()
    conn.close()


# Получение данных пользователя по ID
def get_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id=?', (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    return user_data


# Обновление данных пользователя
def update_user(user_id, name=None, city=None, age=None, descriptions=None, status=None, photo=None):
    conn = get_connection()
    cursor = conn.cursor()
    # Обновляем данные пользователя в таблице
    if name is not None:
        cursor.execute('UPDATE users SET name=? WHERE id=?', (name, user_id))
    if city is not None:
        cursor.execute('UPDATE users SET city=? WHERE id=?', (city, user_id))
    if age is not None:
        cursor.execute('UPDATE users SET age=? WHERE id=?', (age, user_id))
    if descriptions is not None:
        cursor.execute('UPDATE users SET descriptions=? WHERE id=?', (descriptions, user_id))
    if status is not None:
        cursor.execute('UPDATE users SET status=? WHERE id=?', (status, user_id))
    if photo is not None:
        cursor.execute('UPDATE users SET photo=? WHERE id=?', (photo, user_id))
    conn.commit()
    conn.close()

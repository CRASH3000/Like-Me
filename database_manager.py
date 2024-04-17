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
            photo TEXT,
            gender TEXT,
            state INTEGER,
            telegram_username TEXT
        )
    ''')
    conn.commit()
    conn.close()


# Добавление нового пользователя в базу данных
def add_user(user_id, name=None, city=None, age=None, descriptions=None, status=None, photo=None, gender=None, telegram_username=None, state=None):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (id, name, city, age, descriptions, status, photo, gender, telegram_username, state)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, name, city, age, descriptions, status, photo, gender, telegram_username, state))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"User with id {user_id} already exists.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
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
def update_user(user_id, **kwargs):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        for key, value in kwargs.items():
            cursor.execute(f'UPDATE users SET {key}=? WHERE id=?', (value, user_id))
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()


# Получение состояния пользователя
def get_user_state(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT state FROM users WHERE id=?', (user_id,))
    state = cursor.fetchone()
    conn.close()
    return state[0] if state else None


# Получение имени пользователя Telegram
def get_telegram_username(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT telegram_username FROM users WHERE id=?', (user_id,))
    username = cursor.fetchone()
    conn.close()
    return username[0] if username else None


# Удаление пользователя из базы данных
def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id=?', (user_id,))
    conn.commit()
    conn.close()

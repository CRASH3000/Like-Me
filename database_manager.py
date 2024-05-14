import sqlite3

from main import STATE_SEARCHING, STATE_PROFILE


# Подключение к базе данных (или ее создание, если она не существует)
def get_connection():
    return sqlite3.connect("users_database.db")


# Создание таблицы, если она еще не создана
def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
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
    """
    )
    # таблица для хранения лайков и дизлайков
    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS likes (
                user_id INTEGER,
                liked_user_id INTEGER,
                PRIMARY KEY (user_id, liked_user_id),
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (liked_user_id) REFERENCES users (id)
            )
        """
    )
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS viewed_profiles (
    user_id INTEGER,
    viewed_user_id INTEGER,
    PRIMARY KEY (user_id, viewed_user_id)
    )
    """
    )
    cursor.execute(
        """
    Create TABLE IF NOT EXISTS queued_profiles (
    user_id INTEGER,
    queued_user_id INTEGER,
    PRIMARY KEY (user_id, queued_user_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (queued_user_id) REFERENCES users(id)
    )
    """
    )
    conn.commit()
    conn.close()


# Добавление нового пользователя в базу данных
def add_user(
    user_id,
    name=None,
    city=None,
    age=None,
    descriptions=None,
    status=None,
    photo=None,
    gender=None,
    telegram_username=None,
    state=None,
):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO users (id, name, city, age, descriptions, status, photo, gender, telegram_username, state)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                user_id,
                name,
                city,
                age,
                descriptions,
                status,
                photo,
                gender,
                telegram_username,
                state,
            ),
        )
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
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    return user_data


def mark_profile_as_viewed(user_id, viewed_user_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO viewed_profiles (user_id, viewed_user_id) VALUES (?, ?)",
            (user_id, viewed_user_id),
        )
        conn.commit()
        print("Запись добавлена или уже существовала:", user_id, viewed_user_id)
    except Exception as e:
        print(f"Ошибка при добавлении в базу данных: {e}")
    finally:
        conn.close()


# Получение случайного пользователя
def get_random_user(user_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        # Исключаем пользователей, чьи профили уже были просмотрены
        cursor.execute(
            """
            SELECT * FROM users 
            WHERE id NOT IN (
                SELECT viewed_user_id FROM viewed_profiles WHERE user_id=?
            )
            AND id != ?  
            ORDER BY RANDOM() 
            LIMIT 1
        """,
            (user_id, user_id),
        )
        user_data = cursor.fetchone()
        return user_data
    finally:
        conn.close()


# Обновление данных пользователя
def update_user(user_id, **kwargs):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        for key, value in kwargs.items():
            cursor.execute(f"UPDATE users SET {key}=? WHERE id=?", (value, user_id))
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()


# Получение состояния пользователя
def get_user_state(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT state FROM users WHERE id=?", (user_id,))
    state = cursor.fetchone()
    conn.close()
    return state[0] if state else None


# Получение имени пользователя Telegram
def get_telegram_username(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT telegram_username FROM users WHERE id=?", (user_id,))
    username = cursor.fetchone()
    conn.close()
    return username[0] if username else None


# Добавление лайка в базу данных
def add_like(user_id, liked_user_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO likes (user_id, liked_user_id)
            VALUES (?, ?)
        """,
            (user_id, liked_user_id),
        )
        conn.commit()

        if get_user_state(liked_user_id) == STATE_SEARCHING:
            cursor.execute(
                """
                INSERT OR IGNORE INTO queued_profiles (user_id, queued_user_id)
                VALUES (?, ?)
            """,
                (liked_user_id, user_id),
            )
            conn.commit()

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()


def get_likers(liked_user_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT user_id FROM likes WHERE liked_user_id=?", (liked_user_id,)
        )
        return [row[0] for row in cursor.fetchall()]
    finally:
        conn.close()


def clear_liker_from_queue(liker_id, liked_user_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM likes WHERE user_id=? AND liked_user_id=?",
            (liker_id, liked_user_id),
        )
        conn.commit()
    finally:
        conn.close()


def has_like(user_id, liked_user_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT EXISTS(
                SELECT 1 FROM likes WHERE user_id = ? AND liked_user_id = ?
            )
        """,
            (user_id, liked_user_id),
        )
        return cursor.fetchone()[0] == 1
    except Exception as e:
        print(f"Ошибка при проверке лайка: {e}")
        return False
    finally:
        conn.close()


def get_next_profile(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Проверка наличия профилей в очереди
        cursor.execute(
            "SELECT queued_user_id FROM queued_profiles WHERE user_id=? ORDER BY rowid LIMIT 1",
            (user_id,),
        )
        queued_user = cursor.fetchone()
        if queued_user:
            queued_user_id = queued_user[0]
            cursor.execute(
                "DELETE FROM queued_profiles WHERE user_id=? AND queued_user_id=?",
                (user_id, queued_user_id),
            )
            conn.commit()
            return get_user(queued_user_id)

        # Если в очереди нет профилей, ищем случайного пользователя
        return get_random_user(user_id)
    finally:
        conn.close()


# Удаление пользователя из базы данных
def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()


def reset_viewed_profiles(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Удаляем все записи о просмотренных профилях для данного пользователя
        cursor.execute("DELETE FROM viewed_profiles WHERE user_id=?", (user_id,))
        conn.commit()
        print(f"Viewed profiles reset for user {user_id}.")
    except Exception as e:
        print(f"Error resetting viewed profiles for user {user_id}: {e}")
    finally:
        conn.close()


def remove_mutual_likes(user_id, liked_user_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Удаление лайков в обе стороны
        cursor.execute(
            "DELETE FROM likes WHERE (user_id=? AND liked_user_id=?) OR (user_id=? AND liked_user_id=?)",
            (user_id, liked_user_id, liked_user_id, user_id),
        )
        conn.commit()
    except Exception as e:
        print(f"Ошибка при удалении взаимных лайков: {e}")
    finally:
        conn.close()


# Подключение к базе данных
conn = sqlite3.connect("profiles.db")
cursor = conn.cursor()


# функция для фильтрации анкет в соответствии с заданными критериями (пол пользователя)
# def filter_profiles(STATE_PROFILE):
    #conn = sqlite3.connect("users_database.db")
    #cursor = conn.cursor()

    #cursor.execute("SELECT * FROM users WHERE gender != ? AND status = ?", (STATE_PROFILE,))
    #filtered_profiles = cursor.fetchall()

    #conn.close()

    #return filtered_profiles


#  функцию фильтрации для выбора соответствующих анкет.

#filtered_profiles = filter_profiles(STATE_PROFILE)

#for profile in filtered_profiles:
    #print(profile)

import sqlite3

from bot_logic import filters
from main import STATE_SEARCHING


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
            telegram_username TEXT,
            age_filter TEXT,
            city_filter TEXT
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
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS friends (
    user_id INTEGER,
    friend_id INTEGER,
    PRIMARY KEY (user_id, friend_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (friend_id) REFERENCES users(id)
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
            AND id NOT IN (
                SELECT friend_id FROM friends WHERE user_id=?
            )
            AND id != ?  
            ORDER BY RANDOM() 
            LIMIT 1
        """,
            (user_id, user_id, user_id),
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


def get_next_profile(user_id, target_status):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        age_filter = get_age_filter(user_id)
        city_filter = get_city_filter(user_id)

        age_conditions = ""
        city_conditions = ""
        params = [user_id, user_id, user_id, target_status]

        if age_filter != "по умолчанию":
            if '-' in age_filter:
                age_range = age_filter.split('-')
                age_conditions = "AND age BETWEEN ? AND ?"
                params.extend([int(age_range[0]), int(age_range[1])])
            else:
                age_conditions = "AND age = ?"
                params.append(int(age_filter))

        if city_filter != "по умолчанию":
            city_conditions = "AND city = ?"
            params.append(city_filter)

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
        query = f"""
            SELECT * FROM users 
            WHERE id NOT IN (
                SELECT viewed_user_id FROM viewed_profiles WHERE user_id=?
            )
            AND id NOT IN (
                SELECT friend_id FROM friends WHERE user_id=?
            )
            AND id != ?
            AND status = ?
            {age_conditions}
            {city_conditions}
            ORDER BY RANDOM() 
            LIMIT 1
        """
        cursor.execute(query, params)
        user_data = cursor.fetchone()
        return user_data
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


# Функция для удаления взаимных лайков и добавления в друзья
def remove_mutual_likes_and_add_friends(user_id, liked_user_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Удаление лайков в обе стороны
        cursor.execute(
            "DELETE FROM likes WHERE (user_id=? AND liked_user_id=?) OR (user_id=? AND liked_user_id=?)",
            (user_id, liked_user_id, liked_user_id, user_id),
        )

        cursor.execute(
            "INSERT OR IGNORE INTO friends (user_id, friend_id) VALUES (?, ?)",
            (user_id, liked_user_id),
        )
        cursor.execute(
            "INSERT OR IGNORE INTO friends (user_id, friend_id) VALUES (?, ?)",
            (liked_user_id, user_id),
        )

        conn.commit()
    except Exception as e:
        print(f"Ошибка при удалении взаимных лайков и добавлении друзей: {e}")
    finally:
        conn.close()


def get_friends(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT u.id, u.name, u.telegram_username 
            FROM users u 
            JOIN friends f ON u.id = f.friend_id 
            WHERE f.user_id = ?
            """, (user_id,)
        )
        friends = [{"id": row[0], "name": row[1], "username": row[2]} for row in cursor.fetchall()]
        return friends
    except sqlite3.Error as e:
        print(f"Ошибка БД: {e}")
        return []
    finally:
        conn.close()


def add_friend(user_id, friend_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO friends (user_id, friend_id) VALUES (?, ?)",
            (user_id, friend_id),
        )
        cursor.execute(
            "INSERT INTO friends (user_id, friend_id) VALUES (?, ?)",
            (friend_id, user_id),
        )
        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка БД: {e}")
    finally:
        conn.close()


def remove_friend(user_id, friend_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM friends WHERE (user_id=? AND friend_id=?) OR (user_id=? AND friend_id=?)",
            (user_id, friend_id, friend_id, user_id),
        )
        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка БД: {e}")
    finally:
        conn.close()

def set_state(user_id, state):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET state=? WHERE id=?", (state, user_id))
    conn.commit()
    conn.close()

def get_user_state(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT state FROM users WHERE id=?", (user_id,))
    state = cursor.fetchone()
    conn.close()
    return state[0] if state else None

def set_age_filter(user_id, age_filter):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE users SET age_filter=? WHERE id=?", (age_filter, user_id)
        )
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

def get_age_filter(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT age_filter FROM users WHERE id=?", (user_id,))
        age_filter = cursor.fetchone()
        return age_filter[0] if age_filter and age_filter[0] else "по умолчанию"
    finally:
        conn.close()

def set_city_filter(user_id, city_filter):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE users SET city_filter=? WHERE id=?", (city_filter, user_id)
        )
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

def get_city_filter(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT city_filter FROM users WHERE id=?", (user_id,))
    city_filter = cursor.fetchone()
    conn.close()
    return city_filter[0] if city_filter and city_filter[0] else "по умолчанию"




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

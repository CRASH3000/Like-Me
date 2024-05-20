import sqlite3


def get_connection():
    return sqlite3.connect("users_database.db")


# Функция фильтрации пользователей по статусу и полу
def filter_users(user_id, target_status):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT gender, status FROM users WHERE id=?", (user_id,))
        user_data = cursor.fetchone()
        if not user_data:
            return []

        user_gender, user_status = user_data

        query = """
            SELECT * FROM users 
            WHERE id NOT IN (
                SELECT viewed_user_id FROM viewed_profiles WHERE user_id=?
            )
            AND id NOT IN (
                SELECT friend_id FROM friends WHERE user_id=?
            )
            AND id != ?
            AND status = ?
        """
        params = [user_id, user_id, user_id, target_status]

        if user_status == "Найти вторую половинку":
            if user_gender == "Мужчина":
                query += " AND gender = 'Женщина'"
            elif user_gender == "Женщина":
                query += " AND gender = 'Мужчина'"

        query += " ORDER BY RANDOM() LIMIT 1"

        cursor.execute(query, params)
        user_data = cursor.fetchone()
        return user_data
    finally:
        conn.close()
import telebot
from telebot import types
import database_manager

API_TOKEN = '7104369196:AAGZ4NF4cg5bRFdYTnry6chtP8tBoF8j2eA'
bot = telebot.TeleBot(API_TOKEN)

USER_STATE = {}  # Словарь для хранения состояний пользователей
USER_DATA = {}  # Словарь для хранения данных пользователей

# Состояния
STATE_REGISTER = 1
STATE_ENTER_NAME = 2
STATE_ENTER_CITY = 3
STATE_DESCRIPTIONS = 4
STATE_ENTER_AGE = 5
STATE_CHOOSE_STATUS = 6
STATE_UPLOAD_PHOTO = 7
# STATE_PROFILE_PREVIEW = 8
STATE_MAIN_SCREEN = 8


# Функция для обновления состояния пользователя
def set_state(user_id, state):
    USER_STATE[user_id] = state


# Функция для получения состояния пользователя
def get_state(user_id):
    return USER_STATE.get(user_id, None)


# Функция для сохранения данных пользователя
def get_user_data(user_id):
    if user_id not in USER_DATA:
        USER_DATA[user_id] = {}
    return USER_DATA[user_id]


@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Отправка картинки
    img_url = 'https://telegra.ph/file/ad7079ce8110af0f35771.png'
    bot.send_photo(message.chat.id, img_url)

    # Отправка текста с описанием
    # bot.send_message(message.chat.id, "Добро пожаловать! Здесь вы можете зарегистрироваться.")

    # Создание встроенной клавиатуры
    markup = types.InlineKeyboardMarkup()
    reg_button = types.InlineKeyboardButton("Регистрация", callback_data='register')
    markup.add(reg_button)

    # Отправка сообщения с встроенной клавиатурой
    bot.send_message(message.chat.id, "Нажмите на кнопку ниже, чтобы зарегистрироваться: test test test"
                                      "test test test", reply_markup=markup)


# Обработчик для кнопки регистрации
@bot.callback_query_handler(func=lambda call: call.data == 'register')
def handle_registration(call):
    set_state(call.from_user.id, STATE_ENTER_NAME)
    bot.send_message(call.message.chat.id,
                     "Хорошо, перед тем как начать, давай создадим твой профиль. Напиши свое имя.")


# Обработчик текстовых сообщений для регистрации
@bot.message_handler(func=lambda message: get_state(message.from_user.id) == STATE_ENTER_NAME)
def ask_name(message):
    user_data = get_user_data(message.from_user.id)
    user_data['name'] = message.text
    set_state(message.from_user.id, STATE_ENTER_CITY)
    bot.send_message(message.chat.id, "Отлично! Теперь напиши название своего города.")


@bot.message_handler(func=lambda message: get_state(message.from_user.id) == STATE_ENTER_CITY)
def ask_city(message):
    user_data = get_user_data(message.from_user.id)
    user_data['city'] = message.text
    set_state(message.from_user.id, STATE_DESCRIPTIONS)
    bot.send_message(message.chat.id, "Расскажи немного о себе")


@bot.message_handler(func=lambda message: get_state(message.from_user.id) == STATE_DESCRIPTIONS)
def ask_descriptions(message):
    user_data = get_user_data(message.from_user.id)
    user_data['descriptions'] = message.text
    set_state(message.from_user.id, STATE_ENTER_AGE)
    bot.send_message(message.chat.id, "Ок, круто! Сколько тебе лет?")


@bot.message_handler(func=lambda message: get_state(message.from_user.id) == STATE_ENTER_AGE)
def ask_age(message):
    user_data = get_user_data(message.from_user.id)
    try:
        user_data['age'] = int(message.text)
        set_state(message.from_user.id, STATE_CHOOSE_STATUS)

        # Сразу отправляем inline-клавиатуру для выбора статуса
        markup_status = types.InlineKeyboardMarkup()
        buttons = [
            types.InlineKeyboardButton("Найти друзей", callback_data="status_find_friends"),
            types.InlineKeyboardButton("Найти вторую половинку", callback_data='status_find_love'),
            types.InlineKeyboardButton("Просто пообщаться", callback_data='status_just_chat')
        ]
        for button in buttons:
            markup_status.add(button)
        bot.send_message(message.chat.id, "Какую цель общения вы ищете?", reply_markup=markup_status)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите ваш возраст цифрами.")


def get_status_text(callback_data):
    statuses = {
        "status_find_friends": "Найти друзей",
        "status_find_love": "Найти вторую половинку",
        "status_just_chat": "Просто пообщаться",
    }
    # Получаем ключ статуса (например, 'find_friends') и возвращаем соответствующий текст
    return statuses.get(callback_data, "Неизвестный статус")


# Обработка выбора статуса
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if get_state(call.from_user.id) == STATE_CHOOSE_STATUS:
        user_data = get_user_data(call.from_user.id)

        user_data['status'] = get_status_text(call.data)
        set_state(call.from_user.id, STATE_UPLOAD_PHOTO)
        bot.answer_callback_query(call.id) # Подтверждение получения callback_query (запрос обработан)
        bot.send_message(call.message.chat.id, "Теперь загрузите ваше фото.")
    elif call.data == 'go_to_main_menu':  # Условие для обработки кнопки "ОК"
        main_screen(call)


@bot.message_handler(content_types=['photo'],
                     func=lambda message: get_state(message.from_user.id) == STATE_UPLOAD_PHOTO)
def handle_photo_and_final_register(message):
    user_data = USER_DATA.get(message.from_user.id, {})
    photo_id = message.photo[-1].file_id  # Получаем file_id самой большой версии фото
    user_data['photo'] = photo_id

    # Сохраняем все собранные данные в базу данных
    database_manager.add_user(
        name=user_data.get('name'),
        city=user_data.get('city'),
        age=user_data.get('age'),
        descriptions=user_data.get('descriptions'),
        photo=photo_id,
        status=user_data.get('status')
    )

    # Сбрасываем состояние пользователя и отправляем подтверждение об успешной регистрации
    set_state(message.from_user.id, None)

    markup = types.InlineKeyboardMarkup()
    button_ok = types.InlineKeyboardButton("Ок", callback_data="go_to_main_menu")
    markup.add(button_ok)

    bot.send_photo(
        message.chat.id,
        photo_id,
        caption=f"Ваша анкета:\nИмя: {user_data['name']}\nГород: {user_data['city']}"
                f"\nОписание: {user_data['descriptions']}\nЦель общения: {user_data['status']} "
                f"\nВозраст: {user_data['age']}"

    )

    bot.send_message(message.chat.id, "Ваша регистрация успешно завершена!", reply_markup=markup)

    # Очистка временных данных пользователя
    if message.from_user.id in USER_DATA:
        del USER_DATA[message.from_user.id]


@bot.callback_query_handler(func=lambda call: call.data == 'go_to_main_menu')
def main_screen(call):
    set_state(call.from_user.id, STATE_MAIN_SCREEN)
    img_url = 'https://telegra.ph/file/ad7079ce8110af0f35771.png'
    bot.send_photo(call.message.chat.id, img_url)

    markup_main_buttons = types.InlineKeyboardMarkup()
    markup_main_buttons.row(types.InlineKeyboardButton("Начать поиск", callback_data="start_searching"))
    # С помощью метода .row() можно сделать одну большую кнопку

    markup_main_buttons.add(types.InlineKeyboardButton("Мой профиль", callback_data='my_profile'),
                            types.InlineKeyboardButton("О Проекте", callback_data='about_project'))
    # Метод .add() добавляет каждую кнопку в новый ряд, что позволяет сделать в одном ряду две маленькие кнопки

    bot.send_message(call.message.chat.id, "Добро пожаловать на главный экран, тут вы сможете начать поиск "
                                           "спутников, узнать о проекте и настроить свой профиль", reply_markup=markup_main_buttons)


if __name__ == '__main__':
    database_manager.create_table()
    bot.polling(none_stop=True)

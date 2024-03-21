import telebot
from telebot import types

API_TOKEN = 'Token'
bot = telebot.TeleBot(API_TOKEN)

USER_STATE = {}  # Словарь для хранения состояний пользователей
USER_DATA = {}  # Словарь для хранения данных пользователей

# Состояния
STATE_REGISTER = 1
STATE_ENTER_NAME = 2
STATE_ENTER_CITY = 3
STATE_ENTER_AGE = 4
STATE_UPLOAD_PHOTO = 5


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
def ask_city(message):
    user_data = get_user_data(message.from_user.id)
    user_data['name'] = message.text
    set_state(message.from_user.id, STATE_ENTER_CITY)
    bot.send_message(message.chat.id, "Отлично! Теперь напиши название своего города.")


@bot.message_handler(func=lambda message: get_state(message.from_user.id) == STATE_ENTER_CITY)
def ask_age(message):
    user_data = get_user_data(message.from_user.id)
    user_data['city'] = message.text
    set_state(message.from_user.id, STATE_ENTER_AGE)
    bot.send_message(message.chat.id, "Почти закончили. Сколько тебе лет?")

@bot.message_handler(func=lambda message: get_state(message.from_user.id) == STATE_ENTER_AGE)
def ask_photo(message):
    user_data = get_user_data(message.from_user.id)
    try:
        user_data['age'] = int(message.text)  # Проверка, что возраст — это число
        set_state(message.from_user.id, STATE_UPLOAD_PHOTO)  # Переход к состоянию загрузки фото
        bot.send_message(message.chat.id, "Теперь загрузите ваше фото.")
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите ваш возраст цифрами.")

# Отдельный обработчик для получения фото
@bot.message_handler(content_types=['photo'], func=lambda message: get_state(message.from_user.id) == STATE_UPLOAD_PHOTO)
def handle_photo_upload(message):
    user_data = get_user_data(message.from_user.id)
    photo_id = message.photo[-1].file_id  # Получаем file_id самой большой версии фото
    user_data['photo'] = photo_id  # Сохраняем file_id фото в данных пользователя

    # Завершаем регистрацию и выводим все собранные данные
    set_state(message.from_user.id, None)  # Сбрасываем состояние пользователя
    # Используем метод send_photo для отправки фото с подписью
    bot.send_photo(
        message.chat.id,
        photo_id,
        caption=f"Ваша анкета:\nИмя: {user_data['name']}\nГород: {user_data['city']}\nВозраст: {user_data['age']}"
    )


bot.polling(none_stop=True)

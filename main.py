import telebot
from telebot import types
import database_manager

API_TOKEN = 'TOKEN'
bot = telebot.TeleBot(API_TOKEN)

# USER_STATE = {} Словарь для хранения состояний пользователей
USER_DATA = {}  # Словарь для хранения данных пользователей

# Состояния
STATE_ASK_AGE = 1
STATE_ASK_CONSENT = 2
STATE_ENTER_NAME = 3
STATE_ENTER_GENDER = 4
STATE_ENTER_CITY = 5
STATE_DESCRIPTIONS = 6
STATE_CHOOSE_STATUS = 7
STATE_UPLOAD_PHOTO = 8
STATE_MAIN_SCREEN = 9
STATE_ABOUT_PROJECT = 10


# Функция для обновления состояния пользователя
def set_state(user_id, state):
    print(f"Setting state for user {user_id} to {state}")
    try:
        database_manager.update_user(user_id, state=state)
    except Exception as e:
        print(f"Error updating state: {e}")


# Функция для получения состояния пользователя
def get_state(user_id):
    state = database_manager.get_user_state(user_id)
    print(f"State for user {user_id} is {state}")
    return state

# Старт регистрации
@bot.message_handler(commands=['start'])
def send_welcome(message):
    img_url = 'https://telegra.ph/file/ad7079ce8110af0f35771.png'
    bot.send_photo(message.chat.id, img_url)
    markup = types.InlineKeyboardMarkup()
    reg_button = types.InlineKeyboardButton("Регистрация", callback_data='register')
    markup.add(reg_button)
    bot.send_message(message.chat.id, "Нажмите на кнопку ниже, чтобы зарегистрироваться:", reply_markup=markup)


# Обработчик для кнопки регистрации
@bot.callback_query_handler(func=lambda call: call.data == 'register')
def age_request(call):
    user_id = call.from_user.id

    # Создаем пользователя с начальным состоянием в БД
    database_manager.add_user(user_id=user_id, state=STATE_ASK_AGE)
    set_state(user_id, STATE_ASK_AGE)
    bot.send_message(call.message.chat.id, "Перед тем как начать, давай создадим твой профиль. Сколько тебе лет?.")


@bot.message_handler(func=lambda message: get_state(message.from_user.id) == STATE_ASK_AGE)
def age_input(message):
    user_id = message.from_user.id
    try:
        age = int(message.text)
        if age < 16:
            bot.send_message(message.chat.id, "Извини. Но чат-ботом могут пользоваться только лица старше 16 лет.")
            database_manager.delete_user(user_id)  # Удаление пользователя из БД
            set_state(user_id, None)
        else:
            # Добавляем возраст пользователя в БД
            database_manager.update_user(user_id, age=age)
            set_state(user_id, STATE_ASK_CONSENT)
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Да", callback_data="consent_yes"),
                       types.InlineKeyboardButton("Нет", callback_data="consent_no"))
            bot.send_message(message.chat.id,
                             "Для работы с чат-ботом требуется твое разрешение на использование ссылки на ваш профиль. Вы согласны?",
                             reply_markup=markup)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите ваш возраст цифрами.")


@bot.callback_query_handler(func=lambda call: call.data == "consent_yes")
def consent_yes(call):
    user_id = call.from_user.id
    set_state(user_id, STATE_ENTER_NAME)
    bot.send_message(call.message.chat.id,
                     "Хорошо, с формальностями закончили, давай продолжим создавать твой профиль. Как тебя зовут?.")


@bot.callback_query_handler(func=lambda call: call.data == "consent_no")
def consent_no(call):
    user_id = call.from_user.id
    database_manager.delete_user(user_id)  # Удаляем пользователя из БД
    set_state(user_id, None)
    bot.send_message(call.message.chat.id, "Нам жаль, если передумаете, будем ждать вас.")


# Обработчик текстовых сообщений для регистрации
@bot.message_handler(func=lambda message: get_state(message.from_user.id) == STATE_ENTER_NAME)
def ask_name(message):
    user_id = message.from_user.id
    name = message.text
    database_manager.update_user(user_id, name=name)
    set_state(user_id, STATE_ENTER_GENDER)
    markup_gender = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton("Мужчина", callback_data="gender_male"),
        types.InlineKeyboardButton("Женщина", callback_data='gender_female'),
    ]
    for button in buttons:
        markup_gender.add(button)
    bot.send_message(message.chat.id, "Выбери пол", reply_markup=markup_gender)


def get_gender_text(callback_data):
    statuses = {
        "gender_male": "Мужчина",
        "gender_female": "Женщина",
    }
    return statuses.get(callback_data, "Неизвестный пол")


@bot.callback_query_handler(func=lambda call: call.data in ["gender_male", "gender_female"])
def gender_selection(call):
    user_id = call.from_user.id
    gender_text = get_gender_text(call.data)
    database_manager.update_user(user_id, gender=gender_text)
    set_state(user_id, STATE_ENTER_CITY)
    bot.answer_callback_query(call.id)  # подтверждение получения callback
    bot.send_message(call.message.chat.id, "В каком городе ты живешь?")


@bot.message_handler(func=lambda message: get_state(message.from_user.id) == STATE_ENTER_CITY)
def ask_city(message):
    user_id = message.from_user.id
    city = message.text
    database_manager.update_user(user_id, city=city)
    set_state(message.from_user.id, STATE_DESCRIPTIONS)
    bot.send_message(message.chat.id, "Расскажи немного о себе")


@bot.message_handler(func=lambda message: get_state(message.from_user.id) == STATE_DESCRIPTIONS)
def ask_descriptions(message):
    user_id = message.from_user.id
    descriptions = message.text
    database_manager.update_user(user_id, descriptions=descriptions)
    set_state(message.from_user.id, STATE_CHOOSE_STATUS)

    markup_status = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton("Найти друзей", callback_data="status_find_friends"),
        types.InlineKeyboardButton("Найти вторую половинку", callback_data='status_find_love'),
        types.InlineKeyboardButton("Просто пообщаться", callback_data='status_just_chat')
    ]
    for button in buttons:
        markup_status.add(button)
    bot.send_message(message.chat.id, "Какую цель общения вы ищете?", reply_markup=markup_status)


def get_status_text(callback_data):
    statuses = {
        "status_find_friends": "Найти друзей",
        "status_find_love": "Найти вторую половинку",
        "status_just_chat": "Просто пообщаться",
    }
    # Получаем ключ статуса (например, 'find_friends') и возвращаем соответствующий текст
    return statuses.get(callback_data, "Неизвестный статус")


@bot.callback_query_handler(
    func=lambda call: call.data in ["status_find_friends", "status_find_love", "status_just_chat"])
def status_selection(call):
    user_id = call.from_user.id
    status_text = get_status_text(call.data)
    database_manager.update_user(user_id, status=status_text)
    set_state(user_id, STATE_UPLOAD_PHOTO)
    bot.answer_callback_query(call.id)  # подтверждение получения callback
    bot.send_message(call.message.chat.id, "Теперь загрузите ваше фото")


@bot.message_handler(content_types=['photo'],
                     func=lambda message: get_state(message.from_user.id) == STATE_UPLOAD_PHOTO)
def photo_and_final_register(message):
    user_id = message.from_user.id
    photo_id = message.photo[-1].file_id  # Получаем file_id самой большой версии фото
    database_manager.update_user(user_id, photo=photo_id)  # Обновляем профиль пользователя в базе данных с новым фото

    # Сбрасываем состояние пользователя
    set_state(user_id, None)

    # Отправляем текстовое сообщение об успешной регистрации
    bot.send_message(message.chat.id, "Регистрация успешно завершена!",
                     reply_markup=types.InlineKeyboardMarkup().add(
                         types.InlineKeyboardButton("Супер, давай же начнем!", callback_data="show_profile")))


@bot.callback_query_handler(func=lambda call: call.data == "show_profile")
def show_profile(call):
    user_id = call.from_user.id
    user_data = database_manager.get_user(user_id)  # Получаем данные пользователя из базы данных

    if user_data:
        bot.send_photo(
            call.message.chat.id,
            user_data[6],
            caption=f"Ваша анкета:\nИмя: {user_data[1]}\nПол: {user_data[7]}\nГород: {user_data[2]}"
                    f"\nОписание: {user_data[4]}\nЦель общения: {user_data[5]}\nВозраст: {user_data[3]}",
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton("Ок", callback_data="go_to_main_menu"))
        )
    else:
        bot.send_message(call.message.chat.id, "Ошибка при получении данных профиля.")


@bot.callback_query_handler(func=lambda call: call.data == 'go_to_main_menu')
def main_screen(call):
    print("1111")
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
                                           "спутников, узнать о проекте и настроить свой профиль",
                     reply_markup=markup_main_buttons)


@bot.callback_query_handler(func=lambda call: call.data == 'about_project')
def about_project(call):
    print("Handling about_project callback...")
    set_state(call.from_user.id, STATE_ABOUT_PROJECT)
    img_url = 'https://telegra.ph/file/ad7079ce8110af0f35771.png'
    bot.send_photo(call.message.chat.id, img_url, caption="Здесь описание проекта.")

    markup = types.InlineKeyboardMarkup()
    back_button = types.InlineKeyboardButton("Назад", callback_data='go_to_main_menu')
    markup.add(back_button)

    bot.send_message(call.message.chat.id, "Подробнее о проекте...", reply_markup=markup)


if __name__ == '__main__':
    database_manager.create_table()
    bot.polling(none_stop=True)

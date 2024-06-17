from telebot import types
from data_messages import messages
from compatibility_constant import ALL_ZODIAC


# Обработчик для кнопки регистрации
def age_request(call, bot, database_manager, STATE_ASK_AGE):
    user_id = call.from_user.id

    # Создаем пользователя с начальным состоянием в БД
    database_manager.add_user(user_id=user_id, state=STATE_ASK_AGE)
    bot.set_state(user_id, STATE_ASK_AGE)

    age_request_text = messages["age_request_message"]["text"]
    bot.send_message(call.message.chat.id, age_request_text, parse_mode="HTML")


def age_input(message, bot, database_manager, set_state, STATE_ASK_CONSENT):
    user_id = message.from_user.id

    try:
        if len(message.text) > 3:
            error_text = messages["age_input_message"]["error_text_age_over_110"]
            bot.send_message(message.chat.id, error_text)
            return

        age = int(message.text)
        if age < 1 or age > 110:
            error_text = messages["age_input_message"]["error_text_age_over_110"]
            bot.send_message(message.chat.id, error_text, parse_mode="HTML")
        elif age < 16:
            error_text = messages["age_input_message"]["error_text_age_under_16"]
            bot.send_message(message.chat.id, error_text, parse_mode="HTML")
            database_manager.delete_user(user_id)  # Удаление пользователя из БД
            set_state(user_id, None)
        else:
            # Добавляем возраст пользователя в БД
            database_manager.update_user(user_id, age=age)
            set_state(user_id, STATE_ASK_CONSENT)
            consent_text = messages["age_input_message"]["text_consent_messages"]
            button_yes = messages["age_input_message"]["button_text_yes"]
            button_no = messages["age_input_message"]["button_text_no"]

            markup = types.InlineKeyboardMarkup()
            markup.add(
                types.InlineKeyboardButton(button_yes, callback_data="consent_yes"),
                types.InlineKeyboardButton(button_no, callback_data="consent_no"),
            )
            bot.send_message(
                message.chat.id, consent_text, reply_markup=markup, parse_mode="HTML"
            )
    except ValueError:
        error_text = messages["age_input_message"]["error_text_invalid_data_type"]
        bot.send_message(message.chat.id, error_text, parse_mode="HTML")


def button_yes(call, bot, database_manager, set_state, STATE_ENTER_NAME):
    user_id = call.from_user.id
    telegram_username = call.from_user.username
    database_manager.update_user(user_id, telegram_username=telegram_username)

    set_state(user_id, STATE_ENTER_NAME)
    text_yes = messages["consent_yes_message"]["text"]
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text_yes,
        reply_markup=None,
    )  # Удаляем клавиатуру


def button_no(call, bot, database_manager, set_state):
    user_id = call.from_user.id
    database_manager.delete_user(user_id)  # Удаляем пользователя из БД
    set_state(user_id, None)

    text_no = messages["consent_no_message"]["text"]
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text_no,
        reply_markup=None,
    )


# Обработчик текстовых сообщений для регистрации
def gender_request(message, bot, database_manager, set_state, STATE_ENTER_GENDER):
    user_id = message.from_user.id
    name = message.text
    database_manager.update_user(user_id, name=name)
    set_state(user_id, STATE_ENTER_GENDER)

    text_message = messages["ask_gender_message"]["text"]
    button_male = messages["ask_gender_message"]["button_text_male"]
    button_female = messages["ask_gender_message"]["button_text_female"]
    markup_gender = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton(button_male, callback_data="gender_male"),
        types.InlineKeyboardButton(button_female, callback_data="gender_female"),
    ]
    for button in buttons:
        markup_gender.add(button)
    bot.send_message(
        message.chat.id, text_message, reply_markup=markup_gender, parse_mode="HTML"
    )


def get_gender_text(callback_data):
    statuses = {
        "gender_male": "Мужчина",
        "gender_female": "Женщина",
    }
    return statuses.get(callback_data, "Неизвестный пол")


def city_request(call, bot, database_manager, set_state, STATE_ENTER_CITY):
    user_id = call.from_user.id
    gender_text = get_gender_text(call.data)
    database_manager.update_user(user_id, gender=gender_text)
    set_state(user_id, STATE_ENTER_CITY)

    message_text = messages["ask_city_message"]["text"]
    bot.answer_callback_query(call.id)  # подтверждение получения callback
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=message_text,
        reply_markup=None,
        parse_mode="HTML",
    )


def descriptions_request(message, bot, database_manager, set_state, STATE_DESCRIPTIONS):
    user_id = message.from_user.id
    city = message.text
    database_manager.update_user(user_id, city=city)
    set_state(message.from_user.id, STATE_DESCRIPTIONS)

    message_text = messages["ask_descriptions_message"]["text"]
    bot.send_message(message.chat.id, message_text, parse_mode="HTML")


def zodiac_request(message, bot, database_manager, set_state, STATE_ZODIAC):
    """обработчик зз

    Args:
        message (_type_): _description_
        bot (_type_): _description_
        database_manager (_type_): _description_
        set_state (_type_): _description_
        STATE_ZODIAC (_type_): _description_
    """
    user_id = message.from_user.id
    descriptions = message.text
    database_manager.update_user(user_id, descriptions=descriptions)
    markup_status = types.InlineKeyboardMarkup()

    set_state(message.from_user.id, STATE_ZODIAC)
    for zodiac in ALL_ZODIAC:
        btn = types.InlineKeyboardButton(zodiac, callback_data=zodiac)
        markup_status.add(btn)

    message_text = ("🗿 Укажи свой знак зодиака. Поверь это очень важно."
                    "\nВыбери знак зодиака по дате своего дня рождения:"
                    "\n\n* Овен: 21 марта — 20 апреля; "
                    "\n* Телец: 21 апреля — 21 мая; "
                    "\n* Близнецы: 22 мая — 21 июня; "
                    "\n* Рак: 22 июня — 23 июля; "
                    "\n* Лев: 24 июля — 23 августа; "
                    "\n* Дева: 24 августа — 23 сентября; "
                    "\n* Весы: 24 сентября — 23 октября; "
                    "\n* Скорпион: 24 октября — 22 ноября; "
                    "\n* Стрелец: 23 ноября — 22 декабря; "
                    "\n* Козерог: 23 декабря — 20 января; "
                    "\n* Водолей: 21 января — 19 февраля; "
                    "\n* Рыбы: 20 февраля — 20 марта.")
    bot.send_message(
        message.chat.id, message_text, reply_markup=markup_status, parse_mode="HTML"
    )


def status_selection(call, bot, database_manager, set_state, STATE_CHOOSE_STATUS):
    user_id = call.from_user.id
    zodiac_text = call.data
    database_manager.update_user(user_id, zodiac=zodiac_text)

    set_state(user_id, STATE_CHOOSE_STATUS)

    ask_status_data = messages["ask_status_message"]
    message_text = ask_status_data["text"]
    button_status_1 = ask_status_data["button_text_status_1"]
    button_status_2 = ask_status_data["button_text_status_2"]
    button_status_3 = ask_status_data["button_text_status_3"]
    button_status_4 = ask_status_data["button_text_status_4"]

    markup_status = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton(
            button_status_1, callback_data="status_find_friends"
        ),
        types.InlineKeyboardButton(button_status_2, callback_data="status_find_love"),
        types.InlineKeyboardButton(button_status_3, callback_data="status_just_chat"),
        types.InlineKeyboardButton(button_status_4, callback_data="status_business"),
    ]
    for button in buttons:
        markup_status.add(button)

    bot.answer_callback_query(call.id)  # подтверждение получения callback
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=message_text,
        reply_markup=markup_status,
    )


def get_status_text(callback_data):
    statuses = {
        "status_find_friends": "Найти друзей",
        "status_find_love": "Найти вторую половинку",
        "status_just_chat": "Просто пообщаться",
        "status_business": "Найти коллегу или наставника",
    }
    # Получаем ключ статуса (например, 'find_friends') и возвращаем соответствующий текст
    return statuses.get(callback_data, "Неизвестный статус")


def sending_photo(call, bot, database_manager, set_state, STATE_UPLOAD_PHOTO):
    user_id = call.from_user.id
    status_text = get_status_text(call.data)
    database_manager.update_user(user_id, status=status_text)
    set_state(user_id, STATE_UPLOAD_PHOTO)

    message_text = messages["ask_photo_message"]["text"]
    bot.answer_callback_query(call.id)  # подтверждение получения callback
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=message_text,
        reply_markup=None,
    )


def final_request(message, bot, database_manager, set_state, STATE_CREATE_PROFILE):
    user_id = message.from_user.id
    photo_id = message.photo[-1].file_id  # Получаем file_id самой большой версии фото
    database_manager.update_user(
        user_id, photo=photo_id
    )  # Обновляем профиль пользователя в базе данных с новым фото
    set_state(user_id, STATE_CREATE_PROFILE)
    photo_and_final_register_data = messages["photo_and_final_register_message"]
    img_url = photo_and_final_register_data["image_url"]
    message_text = photo_and_final_register_data["text"]
    button = photo_and_final_register_data["button_text"]
    markup = types.InlineKeyboardMarkup()
    reg_button = types.InlineKeyboardButton(button, callback_data="show_profile")
    markup.add(reg_button)
    bot.send_photo(
        message.chat.id,
        img_url,
        caption=message_text,
        reply_markup=markup,
        parse_mode="HTML",
    )

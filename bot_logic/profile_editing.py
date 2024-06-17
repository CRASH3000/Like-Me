import database_manager
from telebot import types
from data_messages import messages


def send_profile_edit_message(message, bot, chat_id, set_state, STATE_EDIT_PROFILE):
    set_state(message.from_user.id, STATE_EDIT_PROFILE)

    edit_profile_data = messages["profile_edit_message"]
    image_url = edit_profile_data["image_url"]
    message_text = edit_profile_data["text2"] + edit_profile_data["text"]
    button_text_back = edit_profile_data["button_text_back"]
    button_text_edit_name = edit_profile_data["button_text_edit_name"]
    button_des = "Описание"
    button_status = "Статус"
    button_city = "Город"
    button_photo = "Фото"

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(button_text_edit_name, callback_data="show_name"),
        types.InlineKeyboardButton(button_des, callback_data="edit_descriptions"),
        types.InlineKeyboardButton(button_status, callback_data="edit_status"),
        types.InlineKeyboardButton(button_city, callback_data="edit_city"),
        types.InlineKeyboardButton(button_photo, callback_data="edit_photo"),
    )
    markup.row(
        types.InlineKeyboardButton(button_text_back, callback_data="show_profile")
    )

    bot.send_photo(
        chat_id,
        photo=image_url,
        caption=message_text,
        parse_mode="HTML",
        reply_markup=markup,
    )


def edit_name(call, bot, set_state, STATE_WAITING_FOR_PROFILE_UPDATE):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    set_state(call.from_user.id, STATE_WAITING_FOR_PROFILE_UPDATE)
    text_message = "✍️ Напиши новое имя \n 👻Хочешь написать свое полное имя или может никнейм или свой псевдоним)"
    bot.send_message(call.message.chat.id, text_message)


def update_name(message):
    user_id = message.from_user.id
    name = message.text
    database_manager.update_user(user_id, name=name)


def update_name_complete(message, bot, set_state, STATUS_PROFILE_UPDATE_COMPLETE):
    set_state(message.chat.id, STATUS_PROFILE_UPDATE_COMPLETE)
    update_name(message)
    send_profile_edit_message(message, bot, set_state, STATUS_PROFILE_UPDATE_COMPLETE)


def edit_descriptions(call, bot, set_state, STATE_WAITING_FOR_DESCRIPTIONS_UPDATE):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    set_state(call.from_user.id, STATE_WAITING_FOR_DESCRIPTIONS_UPDATE)
    text_message = ("Напиши новое описание о себе "
                    "\n👻 Возможно ты хочешь рассказать больше о себе или наоборот что-то сократить")
    bot.send_message(call.message.chat.id, text_message)


def update_descriptions(message):
    user_id = message.from_user.id
    descriptions = message.text
    database_manager.update_user(user_id, descriptions=descriptions)


def update_descriptions_complete(
    message, bot, set_state, STATUS_DESCRIPTIONS_UPDATE_COMPLETE
):
    set_state(message.chat.id, STATUS_DESCRIPTIONS_UPDATE_COMPLETE)
    update_descriptions(message)
    send_profile_edit_message(
        message, bot, set_state, STATUS_DESCRIPTIONS_UPDATE_COMPLETE
    )


def edit_status(call, bot, set_state, STATE_WAITING_FOR_STATUS_UPDATE):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    set_state(call.from_user.id, STATE_WAITING_FOR_STATUS_UPDATE)

    ask_status_data = messages["ask_status_message"]
    message_text = ask_status_data["text"]
    button_status_1 = ask_status_data["button_text_status_1"]
    button_status_2 = ask_status_data["button_text_status_2"]
    button_status_3 = ask_status_data["button_text_status_3"]

    markup_status = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton(
            button_status_1, callback_data="status_find_friends_1"
        ),
        types.InlineKeyboardButton(button_status_2, callback_data="status_find_love_2"),
        types.InlineKeyboardButton(button_status_3, callback_data="status_just_chat_3"),
    ]
    for button in buttons:
        markup_status.add(button)
    bot.send_message(
        call.message.chat.id,
        message_text,
        reply_markup=markup_status,
        parse_mode="HTML",
    )


def update_status_text(callback_data):
    statuses = {
        "status_find_friends_1": "Найти друзей",
        "status_find_love_2": "Найти вторую половинку",
        "status_just_chat_3": "Просто пообщаться",
    }
    # Получаем ключ статуса (например, 'find_friends') и возвращаем соответствующий текст
    return statuses.get(callback_data, "Неизвестный статус")


def update_status_complete(call, bot, set_state, STATUS_UPDATE_COMPLETE):
    user_id = call.from_user.id
    status_text = update_status_text(call.data)
    database_manager.update_user(user_id, status=status_text)
    set_state(call.message.chat.id, STATUS_UPDATE_COMPLETE)
    send_profile_edit_message(
        call, bot, call.message.chat.id, set_state, STATUS_UPDATE_COMPLETE
    )


def edit_city(call, bot, set_state, STATE_WAITING_FOR_CITY_UPDATE):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    set_state(call.from_user.id, STATE_WAITING_FOR_CITY_UPDATE)
    text_message = ("Напиши название своего города  \n👻 <b>Помни что-то нужно указать правильное "
                    "название своего города иначе тебя никто не найдет( </b>")
    bot.send_message(call.message.chat.id, text_message)


def update_city(message):
    user_id = message.from_user.id
    city = message.text
    database_manager.update_user(user_id, city=city)


def update_city_complete(message, bot, set_state, STATE_CITY_UPDATE_COMPLETE):
    set_state(message.chat.id, STATE_CITY_UPDATE_COMPLETE)
    update_city(message)
    send_profile_edit_message(message, bot, set_state, STATE_CITY_UPDATE_COMPLETE)


def edit_photo(call, bot, set_state, STATE_WAITING_FOR_PHOTO_UPDATE):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    set_state(call.from_user.id, STATE_WAITING_FOR_PHOTO_UPDATE)
    text_message = "Отправьте новое фото \n👻 Или картинку, в любом случае тебе решать как украсить свой профиль xD"
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, text_message)


def update_photo(message):
    user_id = message.from_user.id
    photo_id = message.photo[-1].file_id
    database_manager.update_user(user_id, photo=photo_id)


def update_photo_complete(message, bot, set_state, STATE_PHOTO_UPDATE_COMPLETE):
    set_state(message.user_id, STATE_PHOTO_UPDATE_COMPLETE)
    update_photo(message)
    send_profile_edit_message(message, bot, set_state, STATE_PHOTO_UPDATE_COMPLETE)

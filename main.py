import telebot
from telebot import types
import database_manager
import os
from dotenv import load_dotenv
from data_messages import messages
from bot_logic import profile_editing, user_registration, start_bot, add_friends
from compatibility_constant import ALL_ZODIAC, GENDER_IDX, ZODIAC_IDX
import json
import re

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

if API_TOKEN is None:
    print("Ошибка: Токен API не найден.")
else:
    print("Токен API успешно загружен")

with open("compatibility.json", "r", encoding="utf-8") as compatibility_json:
    compatibility = json.load(compatibility_json)

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
STATE_CREATE_PROFILE = 11
STATE_PROFILE = 12
STATE_EDIT_PROFILE = 13
STATE_DELETE_PROFILE = 14
STATE_DELETE_PROFILE_CONFIRM = 15
STATE_WAITING_FOR_PROFILE_UPDATE = 16
STATUS_PROFILE_UPDATE_COMPLETE = 17
STATE_WAITING_FOR_DESCRIPTIONS_UPDATE = 18
STATUS_DESCRIPTIONS_UPDATE_COMPLETE = 19
STATE_WAITING_FOR_STATUS_UPDATE = 20
STATUS_UPDATE_COMPLETE = 21
STATE_WAITING_FOR_CITY_UPDATE = 22
STATE_CITY_UPDATE_COMPLETE = 23
STATE_WAITING_FOR_PHOTO_UPDATE = 24
STATE_PHOTO_UPDATE_COMPLETE = 25
STATE_WAITING_FOR_PHOTO = 26
STATE_SEARCHING = 27
STATE_FILTER_SETTINGS = 28
STATE_CHANGE_AGE_FILTER = 29
STATE_CHANGE_CITY_FILTER = 30
STATE_ZODIAC = 31


def get_compatibility(user_gender, user_zodiac, partner_zodiac):
    return (
        compatibility.get(user_gender.upper())
        .get(user_zodiac.upper())
        .get(partner_zodiac.upper())
    )


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
@bot.message_handler(commands=["start"])
def send_welcome(message):
    start_bot.command_start(message, bot, database_manager, STATE_MAIN_SCREEN)


# Обработчик для кнопки регистрации
@bot.callback_query_handler(func=lambda call: call.data == "register")
def ask_age(call):
    user_registration.age_request(call, bot, database_manager, STATE_ASK_AGE)


@bot.message_handler(
    func=lambda message: get_state(message.from_user.id) == STATE_ASK_AGE
)
def ask_age_handler(message):
    user_registration.age_input(
        message, bot, database_manager, set_state, STATE_ASK_CONSENT
    )


@bot.callback_query_handler(func=lambda call: call.data == "consent_yes")
def consent_yes(call):
    user_registration.button_yes(
        call, bot, database_manager, set_state, STATE_ENTER_NAME
    )


@bot.callback_query_handler(func=lambda call: call.data == "consent_no")
def consent_no(call):
    user_registration.button_no(call, bot, database_manager, set_state)


# Обработчик текстовых сообщений для регистрации
@bot.message_handler(
    func=lambda message: get_state(message.from_user.id) == STATE_ENTER_NAME
)
def ask_gender(message):
    user_registration.gender_request(
        message, bot, database_manager, set_state, STATE_ENTER_GENDER
    )


@bot.callback_query_handler(
    func=lambda call: call.data in ["gender_male", "gender_female"]
)
def ask_city(call):
    user_registration.city_request(
        call, bot, database_manager, set_state, STATE_ENTER_CITY
    )


@bot.message_handler(
    func=lambda message: get_state(message.from_user.id) == STATE_ENTER_CITY
)
def ask_descriptions(message):
    user_registration.descriptions_request(
        message, bot, database_manager, set_state, STATE_DESCRIPTIONS
    )


@bot.message_handler(
    func=lambda message: get_state(message.from_user.id) == STATE_DESCRIPTIONS
)
def ask_zodiac(message):
    """указываем знак зодиака при регистрации

    Args:
        message (_type_): _description_
    """
    user_registration.zodiac_request(
        message, bot, database_manager, set_state, STATE_ZODIAC
    )


@bot.callback_query_handler(func=lambda call: call.data in ALL_ZODIAC)
def ask_status(message):
    user_registration.status_selection(
        message, bot, database_manager, set_state, STATE_CHOOSE_STATUS
    )


@bot.callback_query_handler(
    func=lambda call: call.data
    in [
        "status_find_friends",
        "status_find_love",
        "status_just_chat",
        "status_business",
    ]
)
def ask_photo(call):
    user_registration.sending_photo(
        call, bot, database_manager, set_state, STATE_UPLOAD_PHOTO
    )


@bot.message_handler(
    content_types=["photo"],
    func=lambda message: get_state(message.from_user.id) == STATE_UPLOAD_PHOTO,
)
def photo_and_final_register(message):
    user_registration.final_request(
        message, bot, database_manager, set_state, STATE_CREATE_PROFILE
    )


@bot.callback_query_handler(func=lambda call: call.data == "show_profile")
def show_profile(call):
    user_id = call.from_user.id
    user_data = database_manager.get_user(
        user_id
    )  # Получаем данные пользователя из базы данных
    set_state(user_id, STATE_PROFILE)

    if user_data:
        reply_markup = types.InlineKeyboardMarkup()
        reply_markup.row(
            types.InlineKeyboardButton(
                "Ок, перейти в главное меню", callback_data="go_to_main_menu"
            )
        )
        reply_markup.add(
            types.InlineKeyboardButton(
                "Редактировать профиль", callback_data="edit_profile"
            ),
            types.InlineKeyboardButton(
                "Удалить профиль", callback_data="delete_profile"
            ),
        )

        bot.edit_message_media(
            media=types.InputMediaPhoto(
                user_data[6],
                caption=f"<b>''ВАША АНКЕТА''</b>\n--------------------------------------------------------"
                        f" \nИМЯ:  {user_data[1]}\nПОЛ:  {user_data[7]}\nГОРОД:  {user_data[2]}"
                f"\nОПИСАНИЕ:  {user_data[4]}\nЦЕЛЬ ОБЩЕНИЯ:  {user_data[5]}\nВОЗРАСТ:  {user_data[3]}"
                f"\nЗНАК ЗОДИАКА: {user_data[ZODIAC_IDX]}", parse_mode="HTML"
            ),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=reply_markup,
        )
    else:
        bot.send_message(call.message.chat.id, "Ошибка при получении данных профиля.")


@bot.callback_query_handler(func=lambda call: call.data == "edit_profile")
def edit_profile(call):
    set_state(call.from_user.id, STATE_EDIT_PROFILE)

    edit_profile_data = messages["profile_edit_message"]
    image_url = edit_profile_data["image_url"]
    message_text = edit_profile_data["text"]
    button_text_back = edit_profile_data["button_text_back"]
    button_text_edit_name = edit_profile_data["button_text_edit_name"]
    button_des = "Описание"
    button_status = "Статус"
    button_city = "Город"
    button_photo = "Фото"

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(button_text_edit_name, callback_data="edit_name"),
        types.InlineKeyboardButton(button_des, callback_data="edit_descriptions"),
        types.InlineKeyboardButton(button_status, callback_data="edit_status"),
        types.InlineKeyboardButton(button_city, callback_data="edit_city"),
        types.InlineKeyboardButton(button_photo, callback_data="edit_photo"),
    )
    markup.row(
        types.InlineKeyboardButton(button_text_back, callback_data="show_profile")
    )

    bot.edit_message_media(
        media=types.InputMediaPhoto(image_url, caption=message_text, parse_mode="HTML"),
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup,
    )


@bot.callback_query_handler(func=lambda call: call.data == "edit_name")
def edit_name_callback(call):
    profile_editing.edit_name(call, bot, set_state, STATE_WAITING_FOR_PROFILE_UPDATE)


@bot.message_handler(
    func=lambda message: get_state(message.from_user.id)
    == STATE_WAITING_FOR_PROFILE_UPDATE
)
def update_name_callback(message):
    profile_editing.update_name(message)
    profile_editing.send_profile_edit_message(
        message, bot, message.chat.id, set_state, STATE_EDIT_PROFILE
    )


@bot.callback_query_handler(func=lambda call: call.data == "edit_descriptions")
def edit_descriptions_callback(call):
    profile_editing.edit_descriptions(
        call, bot, set_state, STATE_WAITING_FOR_DESCRIPTIONS_UPDATE
    )


@bot.message_handler(
    func=lambda message: get_state(message.from_user.id)
    == STATE_WAITING_FOR_DESCRIPTIONS_UPDATE
)
def update_descriptions_callback(message):
    profile_editing.update_descriptions(message)
    profile_editing.send_profile_edit_message(
        message, bot, message.chat.id, set_state, STATE_EDIT_PROFILE
    )


@bot.callback_query_handler(func=lambda call: call.data == "edit_status")
def edit_status_callback(call):
    profile_editing.edit_status(call, bot, set_state, STATE_WAITING_FOR_STATUS_UPDATE)


@bot.callback_query_handler(
    func=lambda call: call.data
    in ["status_find_friends_1", "status_find_love_2", "status_just_chat_3"]
)
def update_status_callback(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    profile_editing.update_status_complete(call, bot, set_state, STATE_EDIT_PROFILE)


@bot.callback_query_handler(func=lambda call: call.data == "edit_city")
def edit_city_callback(call):
    profile_editing.edit_city(call, bot, set_state, STATE_WAITING_FOR_CITY_UPDATE)


@bot.message_handler(
    func=lambda message: get_state(message.from_user.id)
    == STATE_WAITING_FOR_CITY_UPDATE
)
def update_city_callback(message):
    profile_editing.update_city(message)
    profile_editing.send_profile_edit_message(
        message, bot, message.chat.id, set_state, STATE_EDIT_PROFILE
    )


@bot.callback_query_handler(func=lambda call: call.data == "edit_photo")
def edit_photo_callback(call):
    profile_editing.edit_photo(call, bot, set_state, STATE_WAITING_FOR_PHOTO_UPDATE)


@bot.message_handler(
    content_types=["photo"],
    func=lambda message: get_state(message.from_user.id)
    == STATE_WAITING_FOR_PHOTO_UPDATE,
)
def update_photo_callback(message):
    profile_editing.update_photo(message)
    profile_editing.send_profile_edit_message(
        message, bot, message.chat.id, set_state, STATE_EDIT_PROFILE
    )


@bot.callback_query_handler(func=lambda call: call.data == "delete_profile")
def confirm_delete_profile(call):
    set_state(call.from_user.id, STATE_DELETE_PROFILE)

    confirm_delete_profile_data = messages["profile_delete_confirm_message"]
    image_url = confirm_delete_profile_data["image_url"]
    message_text = confirm_delete_profile_data["text"]
    button_text_confirm = confirm_delete_profile_data["button_text_confirm_delete"]
    button_text_cancel = confirm_delete_profile_data["button_text_cancel"]

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            button_text_confirm, callback_data="confirm_delete_profile"
        ),
        types.InlineKeyboardButton(button_text_cancel, callback_data="show_profile"),
    )

    bot.edit_message_media(
        media=types.InputMediaPhoto(image_url, caption=message_text, parse_mode="HTML"),
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup,
    )


@bot.callback_query_handler(func=lambda call: call.data == "confirm_delete_profile")
def delete_profile(call):
    database_manager.delete_user(call.from_user.id)
    set_state(call.from_user.id, STATE_DELETE_PROFILE_CONFIRM)

    delete_profile_data = messages["profile_deleted_message"]
    img_url = delete_profile_data["image_url"]
    message_text = delete_profile_data["text"]

    bot.edit_message_media(
        media=types.InputMediaPhoto(img_url, caption=message_text, parse_mode="HTML"),
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
    )

    set_state(call.from_user.id, None)


@bot.callback_query_handler(func=lambda call: call.data == "go_to_main_menu")
def main_screen(call):
    print("1111")
    user_id = call.from_user.id
    notify_likes(user_id)
    set_state(call.from_user.id, STATE_MAIN_SCREEN)

    main_screen_data = messages["main_screen_message"]
    img_url = main_screen_data["image_url"]
    message_text = main_screen_data["text"]
    button_text_start_searching = main_screen_data["button_text_start_searching"]
    button_text_profile = main_screen_data["button_text_profile"]
    button_text_about = main_screen_data["button_text_about"]
    button_text_settings = main_screen_data["button_text_settings"]
    button_text_my_friends = main_screen_data["button_text_my_friends"]

    markup_main_buttons = types.InlineKeyboardMarkup()
    # С помощью метода .row() можно сделать одну большую кнопку
    markup_main_buttons.row(
        types.InlineKeyboardButton(
            button_text_start_searching, callback_data="start_searching"
        )
    )

    markup_main_buttons.add(
        types.InlineKeyboardButton(
            button_text_my_friends, callback_data="show_friends"
        ),
        types.InlineKeyboardButton(
            button_text_settings, callback_data="filter_settings"
        ),
    )
    markup_main_buttons.add(
        types.InlineKeyboardButton(button_text_profile, callback_data="show_profile"),
        types.InlineKeyboardButton(button_text_about, callback_data="about_project"),
    )
    # Метод .add() добавляет каждую кнопку в новый ряд, что позволяет сделать в одном ряду две маленькие кнопки

    bot.edit_message_media(
        media=types.InputMediaPhoto(img_url, caption=message_text, parse_mode="HTML"),
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup_main_buttons,
    )


@bot.callback_query_handler(func=lambda call: call.data == "about_project")
def about_project(call):
    print("Handling about_project callback...")
    set_state(call.from_user.id, STATE_ABOUT_PROJECT)

    about_project_data = messages["about_project_message"]
    img_url = about_project_data["image_url"]
    message_text = about_project_data["text"]
    button_text = about_project_data["button_text_back"]

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(button_text, callback_data="go_to_main_menu"))
    bot.edit_message_media(
        media=types.InputMediaPhoto(img_url, caption=message_text, parse_mode="HTML"),
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup,
    )


# Обработчик для кнопки "Начать поиск"
@bot.callback_query_handler(func=lambda call: call.data == "start_searching")
def start_searching(call):
    user_id = call.from_user.id
    user_data = database_manager.get_user(user_id)
    user_status = user_data[5]
    user_profile = database_manager.get_next_profile(
        user_id, user_status
    )  # Получаем следующего пользователя из базы данных
    main_screen_data = messages["main_screen_message"]
    img_url = main_screen_data["image_url_no_profiles"]
    set_state(user_id, STATE_SEARCHING)

    if user_profile:
        print(f"User data: {user_profile[1]}")

        database_manager.mark_profile_as_viewed(user_id, user_profile[0])

        reply_markup = types.InlineKeyboardMarkup()
        reply_markup.add(
            types.InlineKeyboardButton("💜 Да", callback_data=f"like_{user_profile[0]}"),
            types.InlineKeyboardButton("😈 Нет", callback_data="next_profile"),
        )
        reply_markup.row(
            types.InlineKeyboardButton("Все, хватит", callback_data="go_to_main_menu")
        )
        current_user_gender = user_data[GENDER_IDX]
        current_user_zodiac = user_data[ZODIAC_IDX]
        profile_user_zodiac = user_profile[ZODIAC_IDX]
        current_compatibility = get_compatibility(
            current_user_gender, current_user_zodiac, profile_user_zodiac
        )
        bot.edit_message_media(
            media=types.InputMediaPhoto(
                user_profile[6],
                caption=f"<b>Хотите познакомится?</b>\nИМЯ: {user_profile[1]}\nПОЛ: {user_profile[7]}\nГОРОД: {user_profile[2]}"
                f"\nОПИСАНИЕ: {user_profile[4]}\nЦЕЛЬ ОБЩЕНИЯ: {user_profile[5]}\nВОЗРАСТ: {user_profile[3]}"
                f"\nЗнак зодиака: {user_profile[ZODIAC_IDX]}\nВАША СОВМЕСТИМОСТЬ: {current_compatibility}",
                parse_mode="HTML"
            ),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=reply_markup,
        )
    else:
        reply_markup = types.InlineKeyboardMarkup()
        reply_markup.add(
            types.InlineKeyboardButton(
                "Вернуться в главное меню", callback_data="go_to_main_menu"
            ),
            types.InlineKeyboardButton(
                "Просмотреть анкеты заново", callback_data="restart_searching"
            ),
        )
        bot.edit_message_media(
            media=types.InputMediaPhoto(img_url, caption="👻 Кажется ты посмотрел все доступные анкеты."
                                                         "\n Ты можешь повторно посмотреть анкеты или вернуться "
                                                         "в главное меню."
                                                         "\n\n Кроме этого можешь попробовать поменять свой статус "
                                                         "и настроить фильтры для изменения поиска"),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=reply_markup,
        )


@bot.callback_query_handler(func=lambda call: call.data == "next_profile")
def no_search_profile(call):
    start_searching(call)


# Обработчик для кнопки "Да"
@bot.callback_query_handler(func=lambda call: call.data.startswith("like_"))
def handle_like(call):
    user_id = call.from_user.id
    liked_user_id = int(call.data.split("_")[1])
    main_screen_data = messages["main_screen_message"]
    img_url = main_screen_data["image_url"]

    database_manager.add_like(user_id, liked_user_id)
    send_temporary_confirmation(user_id, "Ваш лайк успешно отправлен!")
    liked_user_data = database_manager.get_user(liked_user_id)

    if check_mutual_like(user_id, liked_user_id):
        user_data = database_manager.get_user(user_id)
        if user_data and liked_user_data:
            send_temporary_confirmation(
                user_id,
                f"👻 Вы понравились друг другу! {liked_user_data[1]} лайкнул вас в ответ. "
                f"Начните общение: @{liked_user_data[9]}",
            )
            send_temporary_confirmation(
                liked_user_id,
                f"👻 Вы понравились друг другу! Вы лайкнули {user_data[1]} Начните общение: @{user_data[9]}",
            )
            database_manager.remove_mutual_likes_and_add_friends(user_id, liked_user_id)

    elif database_manager.get_user_state(liked_user_id) == STATE_MAIN_SCREEN:
        user_data = database_manager.get_user(user_id)
        liked_user_gender = liked_user_data[GENDER_IDX]
        liked_user_zodiac = liked_user_data[ZODIAC_IDX]
        user_zodiac = user_data[ZODIAC_IDX]

        current_compatibility = get_compatibility(
            liked_user_gender, liked_user_zodiac, user_zodiac
        )
        if user_data:
            reply_markup = types.InlineKeyboardMarkup()
            reply_markup.add(
                types.InlineKeyboardButton(
                    "💜 Лайкнуть в ответ",
                    callback_data=f"accept_{user_id}_{liked_user_id}",
                )
            )
            reply_markup.add(
                types.InlineKeyboardButton("😈 Неинтересно", callback_data=f"decline_{user_id}")
            )
            bot.send_photo(
                chat_id=liked_user_id,
                photo=user_data[6],
                caption=f"✉️ <b>Вами заинтересовались!</b>\nИМЯ: {user_data[1]}\nПОЛ: {user_data[7]}\nГОРОД: {user_data[2]}"
                f"\nОПИСАНИЕ: {user_data[4]}\nЦЕЛЬ ОБЩЕНИЯ: {user_data[5]}\nВОЗРАСТ: {user_data[3]}\nВАША СОВМЕСТИМОСТЬ: {current_compatibility}",
                reply_markup=reply_markup, parse_mode="HTML"
            )

    try:
        user_data = database_manager.get_user(user_id)
        user_status = user_data[5]
        next_user_data = database_manager.get_next_profile(user_id, user_status)

        if next_user_data:
            reply_markup = types.InlineKeyboardMarkup()
            reply_markup.add(
                types.InlineKeyboardButton(
                    "💜 Да", callback_data=f"like_{next_user_data[0]}"
                ),
                types.InlineKeyboardButton("😈 Нет", callback_data="next_profile"),
            )
            reply_markup.row(
                types.InlineKeyboardButton(
                    "Все, хватит", callback_data="go_to_main_menu"
                )
            )

            next_user_compatibility = get_compatibility(
                user_gender=user_data[GENDER_IDX],
                user_zodiac=user_data[ZODIAC_IDX],
                partner_zodiac=next_user_data[ZODIAC_IDX],
            )
            bot.edit_message_media(
                media=types.InputMediaPhoto(
                    next_user_data[6],
                    caption=f"👻 <b>Хотите познакомится?</b>\nИМЯ: {next_user_data[1]}\nПОЛ: {next_user_data[7]}\nГОРОД: {next_user_data[2]}"
                    f"\nОПИСАНИЕ: {next_user_data[4]}\nЦЕЛЬ ОБЩЕНИЯ: {next_user_data[5]}\nВОЗРАСТ: {next_user_data[3]}"
                    f"\nЗНАК ЗОДИАКА: {next_user_data[ZODIAC_IDX]}\nВАША СОВМЕСТИМОСТЬ: {next_user_compatibility}",
                    parse_mode="HTML"
                ),
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=reply_markup,
            )
        else:
            markup = types.InlineKeyboardMarkup()
            markup.add(
                types.InlineKeyboardButton(
                    "Вернуться в главное меню", callback_data="go_to_main_menu"
                ),
                types.InlineKeyboardButton(
                    "Просмотреть анкеты заново", callback_data="restart_searching"
                ),
            )
            bot.edit_message_media(
                media=types.InputMediaPhoto(img_url, caption="Нет доступных анкет"),
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=markup,
            )
    except Exception as e:
        print(f"Error: {e}")
        bot.send_message(user_id, "Произошла ошибка при поиске следующего профиля.")


def check_mutual_like(user_id, liked_user_id):
    return database_manager.has_like(
        user_id, liked_user_id
    ) and database_manager.has_like(liked_user_id, user_id)


def notify_likes(user_id):
    likers = database_manager.get_likers(user_id)
    current_user = database_manager.get_user(user_id)
    if current_user:
        current_gender = current_user[GENDER_IDX]
        current_zodiac = current_user[ZODIAC_IDX]

    for liker_id in likers:
        liker_data = database_manager.get_user(liker_id)
        liked_zodiac = liker_data[ZODIAC_IDX]
        reply_markup = types.InlineKeyboardMarkup()
        reply_markup.add(
            types.InlineKeyboardButton(
                "💜 Лайкнуть в ответ", callback_data=f"accept_{user_id}_{liker_id}"
            )
        )
        reply_markup.add(
            types.InlineKeyboardButton("😈 Неинтересно", callback_data=f"decline_{liker_id}")
        )
        current_compatibility = get_compatibility(
            current_gender, current_zodiac, liked_zodiac
        )
        caption = (
            f"✉️ <b>Вами заинтересовались!</b>\nИМЯ: {liker_data[1]}\nПОЛ: {liker_data[7]}\nГОРОД: {liker_data[2]}"
            f"\nОПИСАНИЕ: {liker_data[4]}\nЦЕЛЬ ОБЩЕНИЯ: {liker_data[5]}\nВОЗРАСТ: {liker_data[3]}"
            f"\nВАША СОВМЕСТИМОСТЬ: {current_compatibility}\n",
        )

        bot.send_photo(
            chat_id=user_id,
            photo=liker_data[6],
            caption=caption,
            reply_markup=reply_markup,
            parse_mode="HTML"
        )


@bot.callback_query_handler(func=lambda call: call.data.startswith("accept_"))
def handle_accept(call):
    # Разделение callback_data для получения ID пользователя и ID лайкнутого пользователя
    _, user_id, liked_user_id = call.data.split("_")
    user_id = int(user_id)
    liked_user_id = int(liked_user_id)

    # Получаем данные обоих пользователей
    user_data = database_manager.get_user(user_id)
    liked_user_data = database_manager.get_user(liked_user_id)

    if user_data and liked_user_data:
        send_temporary_confirmation(
            user_id,
            f"👻 Вы понравились друг другу! {liked_user_data[1]} лайкнул вас в ответ. Начните общение: @{liked_user_data[9]}",
        )
        send_temporary_confirmation(
            liked_user_id,
            f"👻 Вы понравились друг другу! Вы лайкнули {user_data[1]} Начните общение: @{user_data[9]}",
        )

        database_manager.remove_mutual_likes_and_add_friends(user_id, liked_user_id)
        bot.delete_message(
            chat_id=call.message.chat.id, message_id=call.message.message_id
        )


@bot.callback_query_handler(func=lambda call: call.data == "restart_searching")
def restart_searching(call):
    user_id = call.from_user.id
    database_manager.reset_viewed_profiles(user_id)
    start_searching(call)


def send_temporary_confirmation(user_id, message_text):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("ОК", callback_data="delete_message"))
    bot.send_message(user_id, message_text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "delete_message")
def delete_message(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("decline_"))
def handle_decline(call):
    user_id = call.from_user.id
    liked_user_id = int(call.data.split("_")[1])

    database_manager.remove_like(liked_user_id, user_id)
    bot.delete_message(call.message.chat.id, call.message.message_id)


@bot.callback_query_handler(func=lambda call: call.data == "show_friends")
def show_friends(call):
    add_friends.show_friends(call, bot, database_manager)


@bot.callback_query_handler(func=lambda call: call.data.startswith("view_friend_"))
def view_friends(call):
    add_friends.view_friend(call, bot, database_manager)


@bot.callback_query_handler(func=lambda call: call.data.startswith("delete_friend_"))
def delete_friend(call):
    add_friends.delete_friend(call, bot, database_manager)


# Обработчик для кнопки "Настройки"
@bot.callback_query_handler(func=lambda call: call.data == "filter_settings")
def filter_settings(call):
    user_id = call.from_user.id
    database_manager.set_state(user_id, STATE_FILTER_SETTINGS)

    filter_settings_data = messages["filter_settings_message"]
    img_url = filter_settings_data["image_url"]
    message_text = filter_settings_data["text"].format(
        age=database_manager.get_age_filter(user_id),
        city=database_manager.get_city_filter(user_id),
    )
    button_text_age = filter_settings_data["button_text_age"]
    button_text_city = filter_settings_data["button_text_city"]
    button_text_back = filter_settings_data["button_text_back"]
    button_text_reset = filter_settings_data["button_text_reset_settings"]

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(button_text_age, callback_data="change_age_filter")
    )
    markup.add(
        types.InlineKeyboardButton(button_text_city, callback_data="change_city_filter")
    )
    markup.add(
        types.InlineKeyboardButton(button_text_reset, callback_data="reset_settings")
    )
    markup.add(
        types.InlineKeyboardButton(button_text_back, callback_data="go_to_main_menu")
    )

    bot.edit_message_media(
        media=types.InputMediaPhoto(img_url, caption=message_text, parse_mode="HTML"),
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup,
    )


# Обработчик для кнопки "Изменить поиск возраста"
@bot.callback_query_handler(func=lambda call: call.data == "change_age_filter")
def change_age_filter(call):
    user_id = call.from_user.id
    database_manager.set_state(user_id, STATE_CHANGE_AGE_FILTER)
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    bot.send_message(
        user_id,
        "Уточните возраст собеседника для поиска. Вы можете искать людей одного возраста написав например 20 или указать возрастной лимит, например 20 - 30",
    )


@bot.message_handler(
    func=lambda message: database_manager.get_user_state(message.from_user.id)
    == STATE_CHANGE_AGE_FILTER
)
def set_age_filter_handler(message):
    user_id = message.from_user.id
    age_input = message.text.strip()

    if validate_age_input(age_input):
        database_manager.set_age_filter(user_id, age_input)
        bot.send_message(user_id, f"Возрастной фильтр установлен: {age_input}")
        show_filter_settings(message)
    else:
        bot.send_message(
            user_id,
            "Некорректный формат. Укажите возраст в формате '20' или '20 - 30'.",
        )


# Обработчик для кнопки "Изменить поиск города"
@bot.callback_query_handler(func=lambda call: call.data == "change_city_filter")
def change_city_filter(call):
    user_id = call.from_user.id
    database_manager.set_state(user_id, STATE_CHANGE_CITY_FILTER)
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    bot.send_message(
        user_id, "Уточните город собеседника для поиска. Введите название города."
    )


@bot.message_handler(
    func=lambda message: database_manager.get_user_state(message.from_user.id)
    == STATE_CHANGE_CITY_FILTER
)
def set_city_filter_handler(message):
    user_id = message.from_user.id
    city_input = message.text.strip()

    if validate_city_input(city_input):
        database_manager.set_city_filter(user_id, city_input)
        bot.send_message(user_id, f"Фильтр по городу установлен: {city_input}")
        show_filter_settings(message)
    else:
        bot.send_message(user_id, "Некорректный формат. Укажите название города.")


def validate_age_input(age_input):
    if len(age_input) > 6:
        return False

    if age_input.isdigit():
        return int(age_input) <= 200
    elif "-" in age_input:
        age_range = age_input.split("-")
        if len(age_range) == 2 and all(part.strip().isdigit() for part in age_range):
            return int(age_range[0]) <= 200 and int(age_range[1]) <= 200
    return False


def validate_city_input(city_input):
    # Проверка на наличие только букв, цифр, пробелов и тире
    # и ограничение на длину до 30 символов
    return bool(re.match("^[a-zA-Zа-яА-Я0-9\\s-]{1,30}$", city_input))


def show_filter_settings(message):
    user_id = message.from_user.id
    filter_settings_data = messages["filter_settings_message"]
    img_url = filter_settings_data["image_url"]
    message_text = filter_settings_data["text"].format(
        age=database_manager.get_age_filter(user_id),
        city=database_manager.get_city_filter(user_id),
    )
    button_text_age = filter_settings_data["button_text_age"]
    button_text_city = filter_settings_data["button_text_city"]
    button_text_back = filter_settings_data["button_text_back"]
    button_text_reset = filter_settings_data["button_text_reset_settings"]

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(button_text_age, callback_data="change_age_filter")
    )
    markup.add(
        types.InlineKeyboardButton(button_text_city, callback_data="change_city_filter")
    )
    markup.add(
        types.InlineKeyboardButton(button_text_reset, callback_data="reset_settings")
    )
    markup.add(
        types.InlineKeyboardButton(button_text_back, callback_data="go_to_main_menu")
    )

    bot.send_photo(
        chat_id=message.chat.id,
        photo=img_url,
        caption=message_text,
        reply_markup=markup,
        parse_mode="HTML",
    )


# Обработчик для кнопки "Сброс настроек"
@bot.callback_query_handler(func=lambda call: call.data == "reset_settings")
def reset_settings(call):
    user_id = call.from_user.id

    # Удаляем фильтры из базы данных (предполагаем, что set_age_filter и set_city_filter удаляют запись, если передать None)
    database_manager.set_age_filter(user_id, None)
    database_manager.set_city_filter(user_id, None)

    # Уведомляем пользователя о сбросе настроек
    # bot.send_message(chat_id=call.message.chat.id, text="Настройки фильтров были сброшены до изначальных значений.")

    # Возвращаемся в меню настроек, чтобы пользователь видел обновленные значения
    filter_settings(call)


if __name__ == "__main__":
    database_manager.create_table()
    print("Бот запущен")
    bot.polling(none_stop=True)

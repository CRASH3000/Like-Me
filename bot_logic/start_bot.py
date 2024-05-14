from telebot import types
from data_messages import messages


def command_start(message, bot, database_manager, STATE_MAIN_SCREEN):
    user_id = message.from_user.id
    user_data = database_manager.get_user(user_id)

    if user_data:
        bot.set_state(user_id, STATE_MAIN_SCREEN)
        main_screen_data = messages["main_screen_message"]
        img_url = main_screen_data["image_url"]
        message_text = main_screen_data["text"]
        button_text_start_searching = main_screen_data["button_text_start_searching"]
        button_text_profile = main_screen_data["button_text_profile"]
        button_text_about = main_screen_data["button_text_about"]

        markup_main_buttons = types.InlineKeyboardMarkup()
        markup_main_buttons.row(
            types.InlineKeyboardButton(
                button_text_start_searching, callback_data="start_searching"
            )
        )
        markup_main_buttons.add(
            types.InlineKeyboardButton(
                button_text_profile, callback_data="show_profile"
            ),
            types.InlineKeyboardButton(
                button_text_about, callback_data="about_project"
            ),
        )

        bot.send_photo(
            message.chat.id,
            img_url,
            caption=message_text,
            reply_markup=markup_main_buttons,
            parse_mode="HTML",
        )

    else:
        welcome_data = messages["welcome_message"]
        img_url = welcome_data["image_url"]
        message_text = welcome_data["text"]
        button_text = welcome_data["button_text"]

        markup = types.InlineKeyboardMarkup()
        reg_button = types.InlineKeyboardButton(button_text, callback_data="register")
        markup.add(reg_button)
        bot.send_photo(
            message.chat.id,
            img_url,
            caption=message_text,
            reply_markup=markup,
            parse_mode="HTML",
        )

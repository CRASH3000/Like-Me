from telebot import types
from data_messages import messages


def show_friends(call, bot, database_manager):
    user_id = call.from_user.id
    friends = database_manager.get_friends(user_id)
    my_friends_message = messages['my_friends_message']
    img_url = my_friends_message['image_url']
    button_text_search = my_friends_message['button_text_search']
    button_text_back = my_friends_message['button_text_back']
    text_no_friends = my_friends_message['text_no_friends']
    if not friends:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(button_text_search, callback_data="start_searching"))
        markup.add(types.InlineKeyboardButton(button_text_back, callback_data="go_to_main_menu"))
        bot.edit_message_media(
            media=types.InputMediaPhoto(img_url, caption=text_no_friends, parse_mode='HTML'),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=markup
        )
    else:
        friends_list_message = "Ваш список друзей:\n"
        markup = types.InlineKeyboardMarkup()
        for friend in friends:
            friends_list_message += f"{friend['name']} - @{friend['username']}\n"
            markup.add(
                types.InlineKeyboardButton(
                    f"🔍 {friend['name']}",
                    callback_data=f"view_friend_{friend['id']}"
                ),
                types.InlineKeyboardButton(
                    f"❌ {friend['name']}",
                    callback_data=f"delete_friend_{friend['id']}"
                )
            )
        markup.add(types.InlineKeyboardButton(button_text_back, callback_data="go_to_main_menu"))
        bot.edit_message_media(
            media=types.InputMediaPhoto(img_url, caption=friends_list_message, parse_mode='HTML'),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=markup
        )


def view_friend(call, bot, database_manager):
    friend_id = int(call.data.split("_")[2])
    user_data = database_manager.get_user(friend_id)

    if user_data:
        reply_markup = types.InlineKeyboardMarkup()
        reply_markup.add(
            types.InlineKeyboardButton("Назад", callback_data="show_friends")
        )
        bot.edit_message_media(
            media=types.InputMediaPhoto(
                user_data[6],
                caption=f"Анкета друга:\nИмя: {user_data[1]}\nПол: {user_data[7]}\nГород: {user_data[2]}"
                f"\nОписание: {user_data[4]}\nЦель общения: {user_data[5]}\nВозраст: {user_data[3]}",
            ),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=reply_markup,
        )
    else:
        bot.send_message(call.message.chat.id, "Ошибка при получении данных анкеты друга.")


def delete_friend(call, bot, database_manager):
    user_id = call.from_user.id
    friend_id = int(call.data.split("_")[2])
    database_manager.remove_friend(user_id, friend_id)
    show_friends(call, bot, database_manager)


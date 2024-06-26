# messages.py

messages = {
    "welcome_message": {
        "image_url": "https://disk.yandex.ru/i/YmJtOMn9mQVpfg",
        "text": "✨ Привет!"
                "\nЯ - телеграмм бот <b>Like me</b> 👻 "
                "\nТвой персональный помощник в поиске новых знакомств и, "
        "возможно, даже любви! Я помогу тебе найти единомышленников, общаться и встречаться с интересными "
        "людьми. \n\nДавай начнем искать тебе идеального собеседника? \nЕсли да, то ответь пожалуйста на "
        "<b>два формальных вопроса.</b>",
        "button_text": "Регистрация",
    },
    "age_request_message": {
        "text": "Перед тем как начать, давай создадим твой профиль. "
        "Напиши, сколько тебе лет 🎂 \n\n<b>*Напиши возраст в цифрах.</b> "
    },
    "age_input_message": {
        "error_text_age_under_16": "Извини, но ботом могут пользоваться только лица старше <b>16 лет.</b>",
        "error_text_age_over_110": "😑Эмм... Вы уверены, что ввели реальный возраст введя цифры?",
        "error_text_invalid_data_type": "Пожалуйста, введите ваш возраст цифрами.",
        "text_consent_messages": "🧐 Для работы с ботом требуется твоё <b>разрешение</b> на использование ссылки "
        "на твой Telegram профиль. Можно?",
        "button_text_yes": "Да 👍",
        "button_text_no": "Нет 👎",
    },
    "consent_yes_message": {
        "text": "Хорошо, с формальностями закончили, давай продолжим создавать твой профиль 😃\n\n Как тебя зовут?"
    },
    "consent_no_message": {"text": "Нам жаль, если передумаешь, будем ждать тебя 😔"},
    "ask_gender_message": {
        "text": "Приятно познакомиться! \nТеперь выбери свой пол.",
        "button_text_male": "Мужчина 🧢",
        "button_text_female": "Женщина 👒",
    },
    "ask_city_message": {
        "text": "В каком городе ты живешь? \n\n*Напиши <b>существующий город</b>, иначе поиск будет некорректным. "
    },
    "ask_descriptions_message": {
        "text": "Расскажи немного о себе 📝 \n\n <b>*НЕ используй стикеры!</b> "

    },
    "ask_status_message": {
        "text": "Какую цель общения ты ищешь?",
        "button_text_status_1": "👋 Найти друзей",
        "button_text_status_2": "💕 Найти вторую половинку",
        "button_text_status_3": "💬 Просто пообщаться",
        "button_text_status_4": "🏦 Найти коллегу или наставника",
    },
    "ask_photo_message": {"text": "Теперь загрузи своё фото 🖼"},
    "photo_and_final_register_message": {
        "image_url": "https://disk.yandex.ru/i/PYfU0S40NbggNQ",
        "text": "🗒 Твой профиль создан! \nТеперь ты можешь начать пользоваться ботом",
        "button_text": "Супер, давай начнем!",
    },
    "profile_edit_message": {
        "image_url": "https://disk.yandex.ru/i/BVzEiuP7fdyY4w",
        "text": "\n👻 Что-то хочешь отредактировать в своем профиле?",
        "button_text_back": "Назад",
        "button_text_edit_name": "Имя",
        "text2": "<b>Данные успешной обновлены!</b>",
    },
    "profile_delete_confirm_message": {
        "image_url": "https://disk.yandex.ru/i/-KkkUr0mvpdh9A",
        "text": "Ты точно хочешь удалить свой профиль? \n<b>Это действие отменить нельзя</b>",
        "button_text_confirm_delete": "✅ Да, удалить",
        "button_text_cancel": "❌ Нет, вернуться назад",
    },
    "profile_deleted_message": {
        "image_url": "https://disk.yandex.ru/i/5SsB5asCqlOYjg",
        "text": "Твой профиль удален. \nНам жаль, что ты уходишь 😞. \nЕсли передумаешь, мы будем рады тебя видеть.",
    },
    "main_screen_message": {
        "image_url": "https://disk.yandex.ru/i/YmJtOMn9mQVpfg",
        "image_url_no_profiles": "https://disk.yandex.ru/i/g5wrfqHed6vQNA",
        "text": "👻 Приветствую тебя, <b>друууг!</b>"
                "\nГотов завести новые знакомства? Я всегда готов помочь тебе в этом."
                "\n\nПомни, ты всегда можешь начать искать себе новых товарищей для конкретной цели."
                "\n\nИ чуть не забыл: если тебе кто-то не ответил взаимностью, не расстраивайся. Здесь полно людей,"
                "которые хотят завести новые знакомства.",
        "button_text_start_searching": "🔍 Начать поиск 🔍",
        "button_text_profile": "🪪 Мой профиль",
        "button_text_my_friends": "👥 Мои друзья",
        "button_text_settings": "⚙️ Настройки поиска",
        "button_text_about": "ℹ️ О Проекте",
    },
    "about_project_message": {
        "image_url": "https://disk.yandex.ru/i/YmJtOMn9mQVpfg",
        "text": " <b>'Like me'</b> - это телеграмм бот полезных знакомств, разработанный с большой "
        "любовью для пользователей. \nЗдесь ты можешь найти новых друзей, партнеров "
        "или просто пообщаться с интересными людьми. "
        "\n\n<b>Преимущества 'Like me' </b> включают в себя удобный и "
        "понятный интерфейс, возможность выбрать цель знакомства. \n\n<b>Главное "
        "преимущество</b> проекта - он <b>полностью бесплатный</b>, так что "
        "присоединяйся и наслаждайся общением! "
        "\n\nС любовью, команда 'Like me' 💙️",
        "button_text_back": "Назад",
        "button_text_stickers": "👻 Получить стикеры",
    },
    "my_friends_message": {
        "image_url": "https://disk.yandex.ru/i/ctH4SohOX7P_RA",
        "button_text_search": "Начать поиск собеседника",
        "button_text_back": "Назад",
        "text_no_friends": "Здесь пока никого нет 🙁",
    },
    "filter_settings_message": {
        "image_url": "https://disk.yandex.ru/i/d4dYB7DbcFi0Bg",
        "text": "👻 тут ты можешь сузить свой круг поиска, указав определенные фильтры или сделать как было)"
                "\n  • <b>Возраст:</b> {age}\n  • <b>Город:</b> {city}",
        "button_text_age": "Изменить поиск возраста",
        "button_text_city": "Изменить поиск города",
        "button_text_reset_settings": "Сбросить настройки",
        "button_text_back": "Назад",
    },
}

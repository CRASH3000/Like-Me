import database_manager

database_manager.create_table()

test_user = [
    (
        1,
        "Нед Фландерс",
        "Спрингфилд",
        60,
        "Чрезвычайно энтузиастичный, глубоко религиозный, известный своим добрососедством.",
        "Найти друзей",
        "https://upload.wikimedia.org/wikipedia/ru/thumb/8/84/Ned_Flanders.png/220px-Ned_Flanders.png",
        "Мужчина",
        "ned_flanders",
        None,
    ),
    (
        2,
        "Питер Гриффин",
        "Куахог",
        45,
        "Люблю веселье, иногда немного тормознут, обожает приключения.",
        "Найти друзей",
        "https://img.kupigolos.ru/hero/5d0fe51431d62.jpg?p=bh&s=368b3c84ea828d8be9a50cd62fc9644d",
        "Мужчина",
        "Peter_Griffin",
        None,
    ),
    (
        3,
        "Тоф Бейфонг",
        "Гаолин",
        16,
        "Хочешь обнять кого-то – обними дерево.",
        "Найти друзей",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ1pgn0f9X26q-Odaqs2UMbV4hJUHFfjVJtouQhDus2iBh7cmjAWqGle75Tex2s8PxCUUM&usqp=CAU",
        "Мужчина",
        "Toph",
        None,
    ),
    [
        4,
        "Венди Кордрой",
        "Гравити Фолз",
        16,
        "Крутая, расслабленная, немного бунтарка. Люблю проводить время с друзьями.",
        "Найти друзей",
        "https://pm1.aminoapps.com/7210/489334476f37190e0bb61423e134647d773c7168r1-1920-1080v2_uhq.jpg",
        "Мужчина",
        "Wendy",
        None,
    ],
]

for user in test_user:
    database_manager.add_user(*user)

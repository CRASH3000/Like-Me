# Дневник разработки по предмету "Проектно-исследовательская работа" (ТюмГУ)
* Учебный проект: Telegram чат бот для знакомств 
* Личный дневник: Ильиных Елизавета
- [GitHub Repository](https://github.com/CRASH3000/Like-Me)
- [Kaiten](https://contact-bot.kaiten.ru/space/321143)

**11.02.2024**
---
**Начало проекта**

Созвонились с коллегами по проекту, определились с проектом. Выбрали Telegram чат бот для знакомств. Поискали ссылки на различные источники информации. Что нашли:
- [Командная разработка ](https://www.atlassian.com/ru/git/tutorials/comparing-workflows/gitflow-workflow)

Создали документы:
- [Команда продукта](https://docs.google.com/document/d/1JcAl_0McW78sLERkTZMMYu67SPoulImLVBCMSDiMRUM/edit?usp=sharing)
- [Workflow продукта](https://docs.google.com/document/d/1IYm_5-bMbct6EAPjuCC8hUipMM-bYcxgWpJFwOk1Te0/edit?usp=sharing)

Создали репозиторий и доску для задач
Важные ссылки:
- [GitHub Repository](https://github.com/CRASH3000/Like-Me)
- [Kaiten](https://contact-bot.kaiten.ru/space/321143)

**12.02.2024**
---
**Созвон с коллегами по проекту**

Обсудили какие фичи будут в проекте, кто будет отвечать за те или иные задачи. 
Я отвечаю за тестирование и улучшение функционала.

 **18.02.2024**
---
**Созвон с коллегами по проекту**

Лид разработки выдал доступы к доске, разбиралась с тем, как ставить задачки и дедлайны в Kaiten

**22.02.2024**
---
**Созвон с коллегами по проекту**

Обсудили, кто какими задачами занят и что можно улучшить в процессах.

**28.02.2024**
---
**Поиск информации о ручном и автоматическом тестировании**

Нашла несколько ссылок:
- [Как и зачем тестировать голосовых и чат-ботов?](https://habr.com/ru/companies/just_ai/articles/706904/)
- [Как протестировать чат-бота](https://www.chatcompose.com/ru/testchatbots.html)

**14.03.2024**
---
**Выбор лого и названия на созвоне**

Команда дискавери представила на выбор варианты лого и названий. На созвоне проголосовали и выбрали. Разбирали на созвоне кто, что сделал.  

**21.03.2024**
---
**Созвон с коллегами**

Команда разработки рассказала, какие задачи сделаны, что предстоит доделать в след спринте

**14.04.2024**
---

**Расписала этапы ручного тестирования**
С появлением прототипа стало ясно, какие именно функции будет предоставлять наш чат-бот. Мы видим, что основные функции включают создание анкеты, поиск других пользователей и процесс мэтчинга (парного сопоставления) пользователей на основе их предпочтений и параметров анкеты.

Чтобы начать ручное тестирование, мы можем составить список тестовых случаев для каждой из этих функций. Ниже представлен пример того, как мы можем разбить тестирование на этапы для каждой функции:

1. Создание анкеты:

Проверка корректности заполнения всех обязательных полей анкеты.
Проверка обработки некорректных данных (например, пустые поля, неверный формат данных).
Проверка сохранения анкеты после ее создания.
Проверка возможности редактирования анкеты после создания.
Проверка отображения созданной анкеты в профиле пользователя.
2. Поиск людей:

Проверка возможности поиска других пользователей по различным критериям (например, возраст, интересы).
Проверка корректности отображения результатов поиска.
Проверка правильности сортировки результатов поиска.
Проверка работы поиска с разными входными данными (например, пустой запрос, некорректные данные).
3. Мэтчинг пользователей:

Проверка корректности алгоритма мэтчинга на основе параметров анкеты и предпочтений пользователей.
Проверка отображения результатов мэтчинга пользователей.
Проверка возможности принятия или отклонения предложенных мэтчей.
Проверка обработки действий пользователя после мэтчинга (например, инициирование чата).
Для каждого тестового случая также важно определить ожидаемый результат, чтобы можно было четко оценить успешность тестирования. Этот список тестовых случаев и их этапы могут быть основой для разработки ручных тестов для нашего чат-бота.

**Занимаюсь тестированием чат-бота**
Нашла несколько багов, сообщила об этом команде

**29.04.2024**
---

**Согласование задач с командой**
С командой выявила для себя задачи:
- Улучшение читаемости кода
- Обучение и повторение ООП
- Разделение модулей согласно ООП

**5.05.2024**
---
**Приступила к задачам**

- Начала с анализа основного кода и выявления мест, которые можно улучшить
- Изучила концпеции ООП, посмотрела как реализуется класс и его функцонал на Python
Найденные ссылки
https://proglib.io/p/python-oop
https://kotazzz.github.io/p/py09/

**12.05.2024**
---

**Выполнение задачи для улучшения читаемости кода**

Изолировала логику запуска бота в отдельный файл, используя принципы ООП для улучшения структуры и расширяемости кода

**14.05.2024**
---

**Выполнение задачи для улучшения читаемости кода**

Сделала рефакторинг кода:
- Создание нового файла user_registration.py, который будет содержать функции и классы, отвечающие за регистрацию пользователей.
Вынесение всей существующей логики регистрации из основного файла main.py в новый файл user_registration.py.
Обеспечение четкого разделения ответственности: файл user_registration.py теперь отвечает только за операции, связанные с регистрацией пользователей, что делает код более модульным и легко поддерживаемым.
- Анализ функций, связанных с регистрацией пользователей, в основном файле main.py и определение тех, которые можно улучшить по названию для лучшей понятности и читаемости.
Переименование функций согласно их функциональности и назначению. 
Обновление всех вызовов этих функций в основном файле main.py с учетом их новых имен, чтобы избежать ошибок при компиляции и выполнении кода.
- Запуск основного файла main.py после проведенного рефакторинга для проверки, что ничего не сломалось.
Внимательное наблюдение за поведением программы и убеждение в том, что все функциональности, связанные с регистрацией пользователей, работают корректно после внесенных изменений.
- Разрешение обнаруженных проблем/ ошибок


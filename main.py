import telebot

# Замените "YOUR_BOT_TOKEN" на токен вашего бота
BOT_TOKEN = "8032815082:AAHM-rLG-FC6n3nBR5PjaYdhS4CfZtTEOig"

bot = telebot.TeleBot(BOT_TOKEN)

# Пример данных для трекинга
tracking_data = {}

# Список ID администраторов
ADMIN_IDS = [1912902102]  # Замените на ваш Telegram ID

# Хранение временных данных для добавления
temp_data = {}


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "🚚🔥Мизоҷи муҳтарам, лутфан трек-коди худро нависед!🚚🔥"
    )


# Обработчик команды для добавления одного трек-кода
@bot.message_handler(commands=['add_track'])
def add_single_track(message):
    if message.from_user.id in ADMIN_IDS:
        bot.send_message(message.chat.id, "🔥Лутфан трек-коди навро ворид кунед🔥:")
        bot.register_next_step_handler(message, process_single_track)
    else:
        bot.send_message(message.chat.id, "❌ Шумо иҷозат надоред барои иловаи трек-код.")


def process_single_track(message):
    track_number = message.text.strip()
    if track_number in tracking_data:
        bot.send_message(message.chat.id, "❌ Ин трек-код аллакай вуҷуд дорад.")
        return

    # Сохраняем трек-код и переходим к запросу даты приёма
    temp_data[message.chat.id] = {"track_number": track_number}
    bot.send_message(message.chat.id, "🔥Лутфан санаи қабул дар Чинро ворид кунед (формат: ДД.ММ.ГГГГ)🔥:")
    bot.register_next_step_handler(message, get_accept_date)


def get_accept_date(message):
    accept_date = message.text.strip()
    temp_data[message.chat.id]["accept_date"] = accept_date
    bot.send_message(message.chat.id, "🔥Лутфан санаи тахминии расидан ба Тоҷикистонро ворид кунед (формат: ДД.ММ.ГГГГ)🔥:")
    bot.register_next_step_handler(message, get_arrival_date)


def get_arrival_date(message):
    arrival_date = message.text.strip()
    data = temp_data.pop(message.chat.id)
    track_number = data["track_number"]

    # Добавляем трек-код в базу с указанными датами
    tracking_data[track_number] = {
        "Трек-номер": track_number,
        "Номер накладной": "1234-5678-90",  # Стандартные данные
        "Дата приема в Китае": data["accept_date"],
        "Примерная дата поступления в Таджикистан": arrival_date,
        "Место выдачи": "Склад Таджикистан",
        "Телефон": "+992927775463",
        "Координаты": "40°18'54.3\"N 69°39'27.6\"E",
    }

    bot.send_message(message.chat.id, f"✅ Трек-код {track_number} успешно добавлен!")
    print(f"Добавлен трек-код: {track_number}")


# Обработчик команды для массового добавления трек-кодов
@bot.message_handler(commands=['add_tracks'])
def add_multiple_tracks(message):
    if message.from_user.id in ADMIN_IDS:
        bot.send_message(
            message.chat.id,
            "🔥Лутфан трек-кодҳоро дар як паём ирсол кунед (ҳар як трек-код бо хатти нав)🔥:"
        )
        bot.register_next_step_handler(message, process_multiple_tracks)
    else:
        bot.send_message(message.chat.id, "❌ Шумо иҷозат надоред барои иловаи трек-код.")


def process_multiple_tracks(message):
    track_numbers = message.text.strip().split("\n")
    temp_data[message.chat.id] = {"track_numbers": track_numbers}
    bot.send_message(message.chat.id, "🔥Лутфан санаи қабул дар Чинро ворид кунед (формат: ДД.ММ.ГГГГ)🔥:")
    bot.register_next_step_handler(message, get_accept_date_for_multiple)


def get_accept_date_for_multiple(message):
    accept_date = message.text.strip()
    temp_data[message.chat.id]["accept_date"] = accept_date
    bot.send_message(message.chat.id, "🔥Лутфан санаи тахминии расидан ба Тоҷикистонро ворид кунед (формат: ДД.ММ.ГГГГ)🔥:")
    bot.register_next_step_handler(message, get_arrival_date_for_multiple)


def get_arrival_date_for_multiple(message):
    arrival_date = message.text.strip()
    data = temp_data.pop(message.chat.id)
    track_numbers = data["track_numbers"]

    added_tracks = 0
    skipped_tracks = 0

    for track_number in track_numbers:
        track_number = track_number.strip()
        if track_number in tracking_data:
            skipped_tracks += 1
            continue
        tracking_data[track_number] = {
            "Трек-номер": track_number,
            "Номер накладной": "1234-5678-90",  # Стандартные данные
            "Дата приема в Китае": data["accept_date"],
            "Примерная дата поступления в Таджикистан": arrival_date,
            "Место выдачи": "Склад Таджикистан",
            "Телефон": "+992927775463",
            "Координаты": "40°15'56.6\"N 69°39'16.4\"E",
        }
        added_tracks += 1

    bot.send_message(
        message.chat.id,
        f"✅ Успешно добавлено: {added_tracks} трек-кодов.\n"
        f"⏩ Пропущено (уже существуют): {skipped_tracks}."
    )
    print(f"Добавлены трек-коды: {tracking_data.keys()}")


# Обработчик для поиска трек-кода
@bot.message_handler(func=lambda message: True)
def track_package(message):
    track_number = message.text.strip()
    if track_number in tracking_data:
        data = tracking_data[track_number]
        coords = data['Координаты'].replace('"', '')
        response = (
            f"📦 *Трек-номер*: {data['Трек-номер']}\n"
            f"🔢 *Номер накладной*: {data['Номер накладной']}\n"
            f"📅 *Дата приема в Китае*: {data['Дата приема в Китае']}\n"
            f"📅 *Примерная дата поступления в Таджикистан*: {data['Примерная дата поступления в Таджикистан']}\n"
            f"📍 *Место выдачи*: {data['Место выдачи']}\n"
            f"📞 *Телефон*: {data['Телефон']}\n"
            f"🌍 *Координаты*: [{data['Координаты']}](https://yandex.ru/maps?whatshere%5Bpoint%5D={coords.replace(' ', '%2C')}&whatshere%5Bzoom%5D=18.395308&ll={coords.replace(' ', '%2C')}&z=18.395308)"
        )
        bot.send_message(message.chat.id, response, parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, "❌ Трек-номер ёфт нашуд. Лутфан дигар трек-кодро ворид намоед.")
        print(f"Трек-код не найден: {track_number}")


if __name__ == "__main__":
    print("Бот запущен!")
    bot.infinity_polling()
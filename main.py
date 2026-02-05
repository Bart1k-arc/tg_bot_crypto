import telebot
from confing import keys, TOKEN
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def start(message):
    text = (
        "💱 Бот-конвертер валют\n\n"
        "Чтобы узнать цену, введи:\n"
        "<валюта 1> <валюта 2> <количество>\n\n"
        "Пример:\n"
        "доллар рубль 100\n\n"
        "Посмотреть доступные валюты: /values"
    )
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["values"])
def values(message):
    text = "📌 Доступные валюты:\n\n"
    for key in keys:
        text += f"🔹 {key}\n"
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=["text"])
def convert(message):
    try:
        values = message.text.lower().split()

        if len(values) != 3:
            raise APIException("Неверный формат.\nВведите: валюта1 валюта2 количество")

        base, quote, amount = values

        price = CryptoConverter.get_price(base, quote, amount)

        bot.send_message(
            message.chat.id,
            f"💰 {amount} {base} = {price:.2f} {quote}"
        )

    except APIException as e:
        bot.send_message(message.chat.id, f"⚠ Ошибка пользователя:\n{e}")

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка сервера:\n{e}")


bot.polling()

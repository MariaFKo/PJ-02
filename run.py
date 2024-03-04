import telebot
from config import TOKEN, CURRENCIES
from extensions import CurrencyConvector, APIException

HELP_TEXT: str = ("Отправите сообщение в виде <имя валюты, цену которой хотите узнать> "
                  "<имя валюты, в которой надо узнать цену первой валюты>"
                  "<количество первой валюты>\nПолучить список доступных валют: /values")

bot = telebot.TeleBot(TOKEN)


# process '/help'
@bot.message_handler(commands=['help'])
def handle_help(message: telebot.types.Message):
    bot.reply_to(message, HELP_TEXT)


# process '/start'
@bot.message_handler(commands=['start'])
def handle_start(message: telebot.types.Message):
    bot.reply_to(message, f"Hi {message.from_user.first_name}!\n" + HELP_TEXT)


# process '/values'
@bot.message_handler(commands=['values'])
def handle_values(message: telebot.types.Message):
    values_text = 'Доступные валюты:\n' + '\n'.join(CURRENCIES)
    bot.reply_to(message, values_text)


# process '/values'
@bot.message_handler(content_types=['text', ])
def currency_convert(message: telebot.types.Message):
    try:
        data = message.text.split()
        if len(data) > 3:
            raise APIException("Превышено количество параметров в запросе")
        elif len(data) < 3:
            raise APIException("Недостаточно параметров для выполнения запроса")
        base, quote, amount = data
        price = CurrencyConvector.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя:\n {e}")
    except Exception as e:
        bot.reply_to(message, f"Неизвестная команда {message.text}\n Ошибка:{e}")
    else:
        text = f'{amount} {base} = {price:10.3f} {quote}'
        bot.reply_to(message, text)


bot.polling(none_stop=True)

import telebot
from config import keys, TOKEN
from extensions import APIExeption, CryptoConverter
# получаем токен
bot = telebot.TeleBot(TOKEN)

# обработка комманды старт
@bot.message_handler(commands=['start'])
def help(message: telebot.types.Message):
    text = 'Здравствуйте \n \'' \
           'Чтобы начать работу, введите комманду боту в следующем формате:\n<имя валюты, цену которой хотите узнать> ' \
           '<имя валюты, в которой хотите узнать цену> ' \
           '<количество первой валюты>\nПросмотреть список валют: /values'
    bot.reply_to(message, text)
# обработка комманды помощь
@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'Для конвертации, введите комманду боту в следующем формате:\n<имя валюты, цену которой хотите узнать> ' \
           '<имя валюты, в которой хотите узнать цену> ' \
           '<количество первой валюты>\nПросмотреть список валют: /values'
    bot.reply_to(message, text)
# обработка комманды получения списка валют
@bot.message_handler(commands=['values'])
def value(message: telebot.types.Message):
    text = 'Доступные валюты:\t'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)
# обработка сообщений конвертации
@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        valus = message.text.split(' ')
        if len(valus) != 3:
            raise APIExeption('Ввод не соответствует формату.\nДля помощи наберите /help')

        quote, base, amount = valus
        total_base = CryptoConverter.get_price(quote, base, amount)
    except APIExeption as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        # print(type(total_base), total_base)
        total_base = total_base * int(amount)
        text = f'Цена {amount} {quote} в {base} будет:\t {total_base}'
        bot.send_message(message.chat.id, text)

# запускаем бот пуллинг
if __name__ == '__main__':
    bot.polling()
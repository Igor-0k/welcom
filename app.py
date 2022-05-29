import telebot
from telebot import types
from config import TOKEN, keys
from extensions import ConvertionExeption, CryptoConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message):
    marcup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Помощь')
    item2 = types.KeyboardButton('Список валют')
    item3 = types.KeyboardButton('Информация')

    marcup.add(item1, item2, item3)

    bot.send_message(message.chat.id, 'Привет! С моей помощью можно конвертировать валюту.'.format(message.from_user),
                     reply_markup=marcup)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'Помощь':
            bot.send_message(message.chat.id, 'Чтобы начать конвертацию, введите команду в формате: '
                                              '\n -Название валюты  '
                                              '\n -В какую валюту перевести  '
                                              '\n -Количество переводимой валюты  '
                             '\n(Через пробел, валюту с большой буквы)')

        elif message.text == 'Список валют':
            for key in keys.keys():
                message.text = '\n'.join((message.text, key,))
            bot.send_message(message.chat.id, message.text)

        elif message.text == 'Информация':
            bot.send_message(message.chat.id, 'Бот использует API с сайта: cryptocompare.com')
        else:
            try:
                value = message.text.split(' ')

                if len(value) != 3:
                    raise ConvertionExeption('Слишком много параметров.')

                quote, base, amount = value
                total_base = CryptoConverter.convert(quote, base, amount)

            except ConvertionExeption as e:
                bot.reply_to(message, f'Ошибка пользователя. \n{e}')

            except Exception as e:
                bot.reply_to(message, f'Не удалось обработать команду\n{e}')

            else:
                text = f'За {amount} - {quote} вы получите \n{total_base * int(amount)} - {base} ' \
                       f'\nпо курсу cryptocompare.com'
                bot.send_message(message.chat.id, text)


bot.polling()
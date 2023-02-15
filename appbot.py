import telebot
from config import keys, TOKEN
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)

# processing of the instructions /start and /help : rules of requests for conversion data


@bot.message_handler(commands=['start', 'help'])
def start_help(message: telebot.types.Message):
    text = 'In order to start input command in the following format:\n<name of base currency> \
<name of target currency> \
<amount of conversion (optional: =1 if None)>\nFor example: dollar euro 20\nIn order to see the list of available currencies input: /values'
    bot.reply_to(message, text)

# processing of the instruction /values : available currencies as output


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Available currencies:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

# processing the user input


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values_list = message.text.split(' ')

        if len(values_list) == 2:
            values_list.append('1')

        if len(values_list) != 3:
            raise APIException('Wrong quantity of parameters!')

        base, quote, amount = values_list

        fx_rate = CurrencyConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'User error!\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Could not process the instruction\n{e}')
    else:
        text = f'Price of {amount}  {base} in {quote} is {fx_rate}'
        bot.send_message(message.chat.id, text)

bot.polling()
import telebot

from setting import *
from extensions import *

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def hendle_start_help(message):
    bot.reply_to(message, start_text)  # Выводим подсказку по управлению ботом


@bot.message_handler(commands=['values'])
def hendle_values(message):  # Показываем список доступных валют
    currencies = 'Доступные валюты:\n'
    for val in value.keys():
        currencies += f"{val}\n"
    bot.send_message(message.chat.id, currencies)


@bot.message_handler(content_types=['text', ])
def change(message):
    try:
        request = message.text.split(" ")  # Разбиваем запрос на список элементов
        request = [x.lower() for x in request]  # Переводим полученный запрос в нижний регистр

        if len(request) != 3:  # Проверка количсетва параметров
            raise APIException('Некорректное число параметров!')

        base, quote, amount = request
        res = ConvertCurrency.get_price(base, quote, amount)  # Вызываем метод и возвращаем из него результат
    except APIException as error:  # Отлавливаем ошибки пользователя и выводим в сообшение
        bot.send_message(message.chat.id, f'Ошибка пользователя:\n{error}\n/help')
    except Exception as error:  # Вывод системных ошибок в сообщения
        bot.send_message(message.chat.id, f"Ошибка сервера:\n{error}")
    else:
        result = f'{amount} {value[base]} в {value[quote]} - {round(res, 2)}\n/help'
        bot.send_message(message.chat.id, result)  # Отправляем результат конвертации пользователю


bot.polling(none_stop=True)

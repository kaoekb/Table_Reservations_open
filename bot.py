import telebot
from config import *
from pymongo import MongoClient
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from random import shuffle
from dateutil.parser import parse
import phonenumbers
bot = telebot.TeleBot(Token_tg)
client = MongoClient(Token_MDB)
db = client["booking"]
questions = db["Questions"]
users = db["Users"]


question_start ={
'question_bot_1': "Вы желаете: ",
'answer_bot_1_a': "Забронировать столик",
'answer_bot_1_b': "Внести изменение в бронь или отказаться от брони",
'answer_bot_1_c': "Другой вопрос",
'back': "Назад",
'question_bot_2': "В какой из наших баров-музеев ваша дружина знатная путь держит? \n <b>Славянский бар-музей “Пьяна Ель”</b> на улице Пестеля, 21 (м. Невский проспект / Маяковская) \n <b>Скандинавский бар-музей “SKAL! Наследие Севера”</b> на улице Правды, 12 (м. Владимирская / Достоевская / Звенигородская)",
'answer_bot_2_a': "Пьяна Ель",
'answer_bot_2_b': "SKAL! Наследие Севера",
'answer_bot_2_c': "Молот ведьм",
}
question_el = {
'question_bot_1': "Вы желаете: ",
'answer_bot_1_a': "Забронировать столик",
'answer_bot_1_b': "Внести изменение в бронь или отказаться от брони",
'answer_bot_1_c': "Другой вопрос",
'back': "Назад",
'question_bot_2': "В какой из наших баров-музеев ваша дружина знатная путь держит? \n <b>Славянский бар-музей “Пьяна Ель”</b> на улице Пестеля, 21 (м. Невский проспект / Маяковская) \n <b>Скандинавский бар-музей “SKAL! Наследие Севера”</b> на улице Правды, 12 (м. Владимирская / Достоевская / Звенигородская)",
'answer_bot_2_a': "Пьяна Ель",
'answer_bot_2_b': "SKAL! Наследие Севера",
'answer_bot_2_c': "там где есть блэкджэк",
'question_bot_3': "Какова численность вашей дружины?",
'question_bot_4': "В какой день ваша дружина желает отобедать?",
'question_bot_5': "В котором часу ожидать вороных? ",
'question_bot_6': "На чье имя доброе оформить бронь?",
'question_bot_7': "Назовите цифры кудесные своего гаджета заморского",
'question_bot_8': "Отмечаете ли вы какое-либо событие (День Рождения, Свадьба и т.д.)",
'answer_bot_8_a': "да",
'answer_bot_8_b': "нет",
'question_bot_8_1': "<i>Для компаний от 8 человек мы предлагаем сделать предзаказ, дабы накрыть столы к их прибытию. Ознакомиться с меню можно здесь - https://barelspb.ru/menu-pdf.</i>",
'answer_bot_8_1_a': "ок",
'question_bot_9': "Стандартное бронирование в нашем баре - 3 часа. Если вы планируете пировать дольше, сообщите об этом"
}
question_skal = {
'question_bot_1': "Вы желаете: ",
'answer_bot_1_a': "Забронировать столик",
'answer_bot_1_b': "Внести изменение в бронь или отказаться от брони",
'answer_bot_1_c': "Другой вопрос",
'back': "Главное меню",
'question_bot_2': "В какой из наших баров-музеев ваша дружина знатная путь держит? \n <b>Славянский бар-музей “Пьяна Ель”</b> на улице Пестеля, 21 (м. Невский проспект / Маяковская) \n <b>Скандинавский бар-музей “SKAL! Наследие Севера”</b> на улице Правды, 12 (м. Владимирская / Достоевская / Звенигородская)",
'answer_bot_2_a': "Пьяна Ель",
'answer_bot_2_b': "SKAL! Наследие Севера",
'answer_bot_2_c': "там где есть блэкджэк",
'question_bot_3': "Сколько мечей в вашем хирде?",
'question_bot_4': "В какой день ожидать драккары?",
'question_bot_5': "В котором часу драккары прибудут к нашим берегам?",
'question_bot_6': "На чье имя доброе оформить захват столика?",
'question_bot_7': "На чей номер знатный оформляем захват?",
'question_bot_8': "Отмечаете ли вы какое-либо событие (День Рождения, Свадьба и т.д.)",
'answer_bot_8_a': "да",
'answer_bot_8_b': "нет",
'question_bot_8_1': "<i>Для компаний от 8 человек мы предлагаем сделать предзаказ, дабы накрыть столы к их прибытию. Ознакомиться с меню можно здесь - https://skalbar.ru/menu.</i>",
'answer_bot_8_1_a': "ок",
'question_bot_9': "Стандартное бронирование в нашем баре - 3 часа. Если вы планируете пировать дольше, сообщите об этом"
}

def is_valid_input(input_str):
    try:
        # Проверка на дату и время
        parse(input_str)
        return True
    except ValueError:
        pass

    try:
        # Проверка на номер телефона
        phonenumbers.parse(input_str)
        return True
    except phonenumbers.phonenumberutil.NumberParseException:
        pass

    # Если вводимые данные не являются датой, временем или номером телефона, вернется значение False
    return False

@bot.message_handler(commands=['start'])
def start_quiz(message):
    bot.send_message(message.chat.id, "Добро пожаловать")
    chat_id = message.chat.id
    user_id = message.from_user.id
    login_tg = message.from_user.username

    user = {
        "chat_id": chat_id,
        'user_id': user_id,
        'login_tg': login_tg,
        "answer1": [],
        "answer2": [],
        "answer3": [],
        "answer4": [],
        "answer5": [],
        "answer6": [],
        "answer7": [],
        "answer8": [],
        "answer9": [],
    }
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(question_start['answer_bot_1_a']))
    markup.add(KeyboardButton(question_start['answer_bot_1_b']))
    markup.add(KeyboardButton(question_start['answer_bot_1_c']))
    
    users.find_one_and_update({"chat_id": chat_id}, {"$setOnInsert": user}, upsert=True)
    bot.send_message(message.chat.id, question_start['question_bot_1'], reply_markup=markup)
    bot.register_next_step_handler(message, lambda m: q1(m) if m.text == question_start['answer_bot_1_a'] else q1_2(m) if m.text == question_start['answer_bot_1_b'] else q1_3(m))



@bot.message_handler(commands=['text'])
def q1(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(question_start['answer_bot_2_a']))
    markup.add(KeyboardButton(question_start['answer_bot_2_b']))
    markup.add(KeyboardButton(question_start['answer_bot_2_c']))
    markup.add(KeyboardButton(question_start['back']))
    answer1 = message.text.lower()
    chat_id = message.chat.id
    users.update_one({"chat_id": chat_id}, {"$set": {"answer1": message.text}})

    bot.send_message(message.chat.id, question_start['question_bot_2'], parse_mode='HTML', reply_markup=markup)
    bot.register_next_step_handler(message, lambda m: q2_el(m) if m.text == question_start['answer_bot_2_a'] else q2_skal(m) if m.text == question_start['answer_bot_2_b'] else q2_3(m) if m.text == question_start['answer_bot_2_c']  else start_quiz(m))


def q2_el(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(question_start['back']))

    answer2 = message.text.lower()
    chat_id = message.chat.id
    users.update_one({"chat_id": chat_id}, {"$set": {"answer2": message.text}})
    bot.send_message(message.chat.id, question_el['question_bot_3'], reply_markup=markup)
    bot.register_next_step_handler(message, lambda m: start_quiz(m) if m.text == question_start['back'] else q3_el(m))

def q3_el(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(question_start['back']))
    answer3 = message.text.lower()
    chat_id = message.chat.id
    if answer3.isdigit():                                                               # Метод isdigit() возвращает True, если все символы в строке являются цифрами. Если нет, возвращается False.
        users.update_one({"chat_id": chat_id}, {"$set": {"answer3": message.text}})
        bot.send_message(message.chat.id, question_el['question_bot_4'], reply_markup=markup)
        bot.register_next_step_handler(message, lambda m: start_quiz(m) if m.text == question_start['back'] else q4_el(m))
    else:
        bot.send_message(chat_id, "Пожалуйста, введите число.")
        bot.register_next_step_handler(message, lambda m: start_quiz(m) if m.text == question_start['back'] else q3_el(m))

def q4_el(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(question_start['back']))
    answer4 = message.text.lower()
    chat_id = message.chat.id
    if is_valid_input(answer4):
        users.update_one({"chat_id": chat_id}, {"$set": {"answer4": message.text}})
        bot.send_message(message.chat.id, question_el['question_bot_5'], reply_markup=markup)
        bot.register_next_step_handler(message, lambda m: start_quiz(m) if m.text == question_start['back'] else q5_el(m))
    else:
        bot.send_message(chat_id, "Пожалуйста, введите число.")
        bot.register_next_step_handler(message, lambda m: start_quiz(m) if m.text == question_start['back'] else q4_el(m))

def q5_el(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(question_start['back']))
    answer5 = message.text.lower()
    chat_id = message.chat.id
    if is_valid_input(answer5):
        users.update_one({"chat_id": chat_id}, {"$set": {"answer5": message.text}})
        bot.send_message(message.chat.id, question_el['question_bot_6'], reply_markup=markup)
        bot.register_next_step_handler(message, lambda m: start_quiz(m) if m.text == question_start['back'] else q6_el(m))
    else:
        bot.send_message(chat_id, "Пожалуйста, введите число.")
        bot.register_next_step_handler(message, lambda m: start_quiz(m) if m.text == question_start['back'] else q5_el(m))

def q6_el(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(question_start['back']))
    answer6 = message.text.lower()
    chat_id = message.chat.id
    users.update_one({"chat_id": chat_id}, {"$set": {"answer6": message.text}})
    bot.send_message(message.chat.id, question_el['question_bot_7'], reply_markup=markup)
    bot.register_next_step_handler(message, lambda m: start_quiz(m) if m.text == question_start['back'] else q7_el(m))

def q7_el(message):
    answer7 = message.text.lower()    
    chat_id = message.chat.id
    if is_valid_input(answer7):
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton(question_el['answer_bot_8_a']))
        markup.add(KeyboardButton(question_el['answer_bot_8_b']))
        markup.add(KeyboardButton(question_start['back']))
        users.update_one({"chat_id": chat_id}, {"$set": {"answer7": message.text}})
        bot.send_message(message.chat.id, question_el['question_bot_8'], reply_markup=markup)
        bot.register_next_step_handler(message, lambda m: q8_1_el(m) if m.text == question_el['answer_bot_8_a'] else start_quiz(m) if m.text == question_start['back'] else q8_el(m))
    else:
        bot.send_message(chat_id, "Пожалуйста, введите число.")
        bot.register_next_step_handler(message, lambda m: start_quiz(m) if m.text == question_start['back'] else q7_el(m))

def q8_el(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(question_start['back']))
    answer8 = message.text.lower()
    chat_id = message.chat.id
    users.update_one({"chat_id": chat_id}, {"$set": {"answer8": message.text}})
    
    bot.send_message(message.chat.id, question_el['question_bot_9'], reply_markup=markup)
    bot.register_next_step_handler(message, lambda m: start_quiz(m) if m.text == question_start['back'] else q9_el(m))

def q8_1_el(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(question_start['back']))
    bot.send_message(message.chat.id, question_el['question_bot_8_1'], parse_mode='HTML')
    chat_id = message.chat.id
    users.update_one({"chat_id": chat_id}, {"$set": {"answer8": message.text}})

    bot.send_message(message.chat.id, question_el['question_bot_9'], reply_markup=markup)
    bot.register_next_step_handler(message, lambda m: start_quiz(m) if m.text == question_start['back'] else q9_el(m))

def q9_el(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(question_start['back']))
    answer9 = message.text.lower()
    chat_id = message.chat.id
    users.update_one({"chat_id": chat_id}, {"$set": {"answer9": message.text}})

    bot.send_message(message.chat.id, "успех, пока мы вас ждем поиграйте в игру @Slavic_quiz_bot", reply_markup=markup)
    bot.register_next_step_handler(message, lambda m: start_quiz(m) if m.text == question_start['back'] else start_quiz(m))

def q1_2(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(question_start['back']))
    answer10 = message.text.lower()
    bot.send_message(message.chat.id, "2.2", reply_markup=markup)
    bot.register_next_step_handler(message, lambda m: start_quiz(m) if m.text == question_start['back'] else start_quiz(m))

def q1_3(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(question_start['back']))
    answer10 = message.text.lower()
    bot.send_message(message.chat.id, "поиграйте в игру @game_of_rapprochement_bot", reply_markup=markup)
    bot.register_next_step_handler(message, lambda m: start_quiz(m) if m.text == question_start['back'] else start_quiz(m))



def q2_skal(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(question_start['back']))
    answer2 = message.text.lower()
    chat_id = message.chat.id
    users.update_one({"chat_id": chat_id}, {"$set": {"answer2": message.text}})

    bot.send_message(message.chat.id, question_skal['question_bot_3'], reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(message, lambda m: start_quiz(m) if m.text == question_start['back'] else q3_skal(m))

def q3_skal(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(question_start['back']))
    answer3 = message.text.lower()
    chat_id = message.chat.id
    if answer3.isdigit():                                                             # Метод isdigit() возвращает True, если все символы в строке являются цифрами. Если нет, возвращается False.
        users.update_one({"chat_id": chat_id}, {"$set": {"answer3": message.text}})
        bot.send_message(message.chat.id, question_skal['question_bot_4'])
        bot.register_next_step_handler(message, lambda m: start_quiz(m) if m.text == question_start['back'] else q4_skal(m))
    else:
        bot.send_message(chat_id, "Пожалуйста, введите число.")
        bot.register_next_step_handler(message, lambda m: start_quiz(m) if m.text == question_start['back'] else q3_skal(m))




def q4_skal(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(question_start['back']))
    answer4 = message.text.lower()
    chat_id = message.chat.id
    if is_valid_input(answer4):
        users.update_one({"chat_id": chat_id}, {"$set": {"answer4": message.text}})
        bot.send_message(message.chat.id, question_skal['question_bot_5'])
        bot.register_next_step_handler(message, lambda m: start_quiz(m) if m.text == question_start['back'] else q5_skal(m))
    else:
        bot.send_message(chat_id, "Пожалуйста, введите число.")
        bot.register_next_step_handler(message, lambda m: start_quiz(m) if m.text == question_start['back'] else q4_skal(m))

def q5_skal(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(question_start['back']))
    answer5 = message.text.lower()
    chat_id = message.chat.id
    if is_valid_input(answer5):
        users.update_one({"chat_id": chat_id}, {"$set": {"answer5": message.text}})
        bot.send_message(message.chat.id, question_skal['question_bot_6'])
        bot.register_next_step_handler(message, lambda m: start_quiz(m) if m.text == question_start['back'] else q6_skal(m))
    else:
        bot.send_message(chat_id, "Пожалуйста, введите число.")
        bot.register_next_step_handler(message, lambda m: start_quiz(m) if m.text == question_start['back'] else q5_skal(m))

def q6_skal(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(question_start['back']))
    answer6 = message.text.lower()
    chat_id = message.chat.id
    users.update_one({"chat_id": chat_id}, {"$set": {"answer6": message.text}})

    bot.send_message(message.chat.id, question_skal['question_bot_7'])
    bot.register_next_step_handler(message, lambda m: start_quiz(m) if m.text == question_start['back'] else q7_skal(m))

def q7_skal(message):
    answer7 = message.text.lower()
    chat_id = message.chat.id
    if is_valid_input(answer7):
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton(question_skal['answer_bot_8_a']))
        markup.add(KeyboardButton(question_skal['answer_bot_8_b']))
        markup.add(KeyboardButton(question_start['back']))
        users.update_one({"chat_id": chat_id}, {"$set": {"answer7": message.text}})
        bot.send_message(message.chat.id, question_skal['question_bot_8'], reply_markup=markup)
        bot.register_next_step_handler(message, lambda m: q8_1_skal(m) if m.text == question_skal['answer_bot_8_a'] else start_quiz(m) if m.text == question_start['back'] else q8_skal(m))
    else:
        bot.send_message(chat_id, "Пожалуйста, введите число.")
        bot.register_next_step_handler(message, lambda m: start_quiz(m) if m.text == question_start['back'] else q7_skal(m))

def q8_skal(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(question_start['back']))
    answer8 = message.text.lower()
    chat_id = message.chat.id
    users.update_one({"chat_id": chat_id}, {"$set": {"answer8": message.text}})
    bot.send_message(message.chat.id, question_skal['question_bot_9'], reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(message, lambda m: start_quiz(m) if m.text == question_start['back'] else q9_skal(m))

def q8_1_skal(message):
    bot.send_message(message.chat.id, question_skal['question_bot_8_1'], parse_mode='HTML')
    chat_id = message.chat.id
    users.update_one({"chat_id": chat_id}, {"$set": {"answer8": message.text}})
    bot.send_message(message.chat.id, question_skal['question_bot_9'], reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(message, q9_skal)

def q9_skal(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(question_start['back']))
    answer9 = message.text.lower()
    chat_id = message.chat.id
    users.update_one({"chat_id": chat_id}, {"$set": {"answer9": message.text}})

    bot.send_message(message.chat.id, "SKAL! Успех, пока мы вас ждем поиграйте в игру @Quiz_Vikings_bot")
    bot.register_next_step_handler(message, lambda m: start_quiz(m) if m.text == question_start['back'] else start_quiz(m))


def q2_3(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(question_start['back']))
    answer10 = message.text.lower()
    bot.send_message(message.chat.id, "Будет еще праздник на нашей улице")
    bot.register_next_step_handler(message, lambda m: start_quiz(m) if m.text == question_start['back'] else start_quiz(m))


bot.polling()



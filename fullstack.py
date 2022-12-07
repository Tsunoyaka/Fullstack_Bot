import telebot
import json
from peewee import *
from setting import settinds
from telebot import types
from decouple import config

db = PostgresqlDatabase(settinds.db)
cursor = db.cursor()
# cursor.execute("DELETE FROM hotel_hotel WHERE stars = 5")
# results = cursor.fetchall()
# # db.close()
# # print(db.get_columns('hotel_hotel'))

# keyboard = types.InlineKeyboardMarkup()
# url_button = types.InlineKeyboardButton(text="Забронировать", url="https://example.com")
# keyboard.add(url_button)

def get_db(db):
    with open(f'{db}.json', 'r') as file:
        return json.load(file)

def write_db(db,data):
    with open(f'{db}.json', 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def get_photo(id):
    with open(f'/home/hello/fullstack_hackathon/media/{id}', 'rb') as f:
        return f.read()

# def find():
#     erdan = 'Erdan'
#     cursor.execute(f"SELECT * FROM hotel_hotel WHERE title LIKE '{erdan}'")
#     results = cursor.fetchall()
#     for i in results:
#         obj = {
#         'title':i[0],
#         'region':i[5],
#         'desc':i[4],
#         }
#         print(i)
#     db.close()
# find()

# def random_hotel():
#     cursor.execute("SELECT * FROM hotel_hotel ORDER BY RANDOM() LIMIT 1")
#     results = cursor.fetchall()
#     for i in results:
#         # obj = {
#         # 'title':i[0],
#         # 'region':i[5],
#         # 'desc':i[4],
#         # 'image':i[6]
#         # }
#         print(i)
#     db.close()

# random_hotel()

def update_hotel():
    get_table = ...
    update = ...
    cursor.execute(f"UPDATE hotel_hotel SET '{get_table}' = '{update}'")
    results = cursor.fetchall()
    db.close()


bot = telebot.TeleBot(config('TOKEN'))




@bot.message_handler(commands=['find'])
def start_message(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id,'Напишите название отеля:')
    bot.register_next_step_handler(msg,find)

def find(message):
    chat_id = message.chat.id
    user_text = message.text
    try:
        cursor.execute(f"SELECT * FROM hotel_hotel WHERE title ILIKE '{user_text}%' LIMIT 1")
        results = cursor.fetchall()
        for i in results:
            photo = get_photo(i[6])
            obj = f"""
{i[0]}

{i[5]}

{i[4]}
            """
        keyboard = types.InlineKeyboardMarkup()
        url_button1 = types.InlineKeyboardButton(text="Забронировать", url=f"http://34.159.95.125/hotel/hotels/{i[2]}")
        keyboard.add(url_button1)
        bot.send_photo(chat_id, photo, caption=obj, reply_markup=keyboard)  
        db.close()
    except:
        bot.send_message(chat_id, 'Отель с таким названием не найден!')


def find_update(message, user_text):
    chat_id = message.chat.id
    try:
        cursor.execute(f"SELECT * FROM hotel_hotel WHERE title ILIKE '{user_text}%' LIMIT 1")
        results = cursor.fetchall()
        for i in results:
            photo = get_photo(i[6])
            obj = f"""
title: {i[0]}

region: {i[5]}

desc: {i[3]}

desc_list: {i[4]}
            """
        # db.close()
        bot.send_photo(chat_id, photo, caption=obj) 
    except:
        bot.send_message(chat_id, 'Ведите корректные данные!')

@bot.message_handler(commands=['random'])
def start_message(message):
    chat_id = message.chat.id
    cursor.execute("SELECT * FROM hotel_hotel ORDER BY RANDOM() LIMIT 1")
    results = cursor.fetchall()
    for i in results:
        photo = get_photo(i[6])
        obj =f"""

{i[0]}

Region: {i[5]}

{i[4]}
"""
        keyboard = types.InlineKeyboardMarkup()
        url_button1 = types.InlineKeyboardButton(text="Забронировать", url=f"http://34.159.95.125/hotel/hotels/{i[2]}")
        keyboard.add(url_button1)
        # keyboard.
        db.close()

    bot.send_photo(chat_id, photo, caption=obj, reply_markup=keyboard)

@bot.message_handler(commands=['update_hotel'])
def start_message(message):
    chat_id = message.chat.id 
    msg = bot.send_message(chat_id,'Название отеля, которое надо обновить:')
    bot.register_next_step_handler(msg, update_hotel_table)

def update_hotel_table(message):
    chat_id = message.chat.id 
    dbj = get_db('update')
    user_text = message.text
    find_update(message, user_text)
    dbj['hotel'] = user_text
    write_db('update',dbj)
    msg = bot.send_message(chat_id,'Название столбца для обновления:')
    bot.register_next_step_handler(msg, update_hotel_column)


def update_hotel_column(message):
    chat_id = message.chat.id 
    user_text = message.text
    dbj = get_db('update')
    dbj['column'] = user_text
    write_db('update', dbj)
    msg = bot.send_message(chat_id, 'Изменить на:')
    bot.register_next_step_handler(msg, update_hotel_final)

def update_hotel_final(message):
    chat_id = message.chat.id 
    user_text = message.text
    dbj = get_db('update')
    cursor.execute(f"UPDATE hotel_hotel SET {dbj['column']} = '{user_text}' WHERE title LIKE '{dbj['hotel']}%';")
    find_update(message, dbj['hotel'])
    msg = bot.send_message(chat_id, 'Успешно обновлено')

    db.close()

@bot.message_handler(commands=['help'])
def start_message(message):
    chat_id = message.chat.id 
    msg = bot.send_message(chat_id,"""
Список доступных комманд:

/find - поиск отеля по названию
/random - случайный отель
/update_hotel - обновление данных отеля
/admin - написать администратору через бота
    """)
    bot.register_next_step_handler(msg, update_hotel_table)

@bot.message_handler(commands=['admin'])
def start_message(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, 'Напишите сообщение администратору:')
    bot.register_next_step_handler(msg, msg_admin)

def msg_admin(message):
    chat_id = message.chat.id
    user_text = message.text
    bot.send_message(config('ADMIN'), user_text)
    bot.send_message(chat_id, 'Успешно! Я перенаправил ваше сообщение администратору.')



bot.polling()

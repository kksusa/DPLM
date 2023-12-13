"""Модуль c функциями/методами взаимодействия с БД."""

import sqlite3
import pandas as pd


# Функция инициализации таблицы Users
def init():
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
    telegram_id INTEGER NOT NULL,
    username TEXT NOT NULL,
    first_name TEXT NOT NULL,
    balance INTEGER NOT NULL,
    cashback INTEGER NOT NULL,
    current_place TEXT,
    survey INTEGER NOT NULL,
    survey_drinks TEXT,
    survey_syrups TEXT,
    survey_drink_tastes TEXT,
    survey_review TEXT
    )
    ''')
    connection.commit()
    connection.close()


# Функция инициализации таблицы Counted_drinks
def init_counted_drinks():
    connection = sqlite3.connect('counted_drinks.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Counted_drinks (
    place TEXT NOT NULL,
    drink TEXT NOT NULL,
    time_hour INTEGER NOT NULL,
    time_minute INTEGER NOT NULL
    )
    ''')
    connection.commit()
    connection.close()


# Функция регистрации пользователя
def add_user(user):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute(
        'INSERT INTO Users (telegram_id, username, first_name, balance, cashback, survey) VALUES (?, ?, ?, ?, ?, ?)',
        user)
    connection.commit()
    connection.close()


# Функция регистрации учтенного напитка по акции "кэшбек"
def add_drink(current_drink):
    connection = sqlite3.connect('counted_drinks.db')
    cursor = connection.cursor()
    cursor.execute(
        'INSERT INTO Counted_drinks (place, drink, time_hour, time_minute) VALUES (?, ?, ?, ?)', current_drink)
    connection.commit()
    connection.close()


# Функция стирания данных из таблицы Counted_drinks
def delete_drinks_table():
    connection = sqlite3.connect('counted_drinks.db')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM Counted_drinks')
    connection.commit()
    connection.close()


# Метод поиска баланса
def find_balance(input_telegram_id):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute("SELECT balance FROM Users WHERE telegram_id = ?", (input_telegram_id,))
    result = cursor.fetchone()
    connection.close()
    return result[0]


# Метод поиска опции cashback
def find_cashback(input_telegram_id):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute("SELECT cashback FROM Users WHERE telegram_id = ?", (input_telegram_id,))
    result = cursor.fetchone()
    connection.close()
    return result[0]


# Метод поиска текущего места
def find_current_place(input_telegram_id):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute("SELECT current_place FROM Users WHERE telegram_id = ?", (input_telegram_id,))
    result = cursor.fetchone()
    connection.close()
    return result[0]


# Метод поиска напитка в таблице Counted_drinks
def find_drinks(current_place, current_drink, current_hour, current_minute):
    connection = sqlite3.connect('counted_drinks.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT place, drink, time_hour, time_minute FROM Counted_drinks
                   WHERE (place = ?) AND (drink = ?) AND (time_hour = ?) AND (time_minute = ?)""",
                   (current_place, current_drink, current_hour, current_minute,))
    result = cursor.fetchall()
    connection.close()
    return result


# Метод поиска опции survey
def find_survey(input_telegram_id):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute("SELECT survey FROM Users WHERE telegram_id = ?", (input_telegram_id,))
    result = cursor.fetchone()
    connection.close()
    return result[0]


# Метод поиска уже учтенных напитков по акции "опрос"
def find_survey_drinks(input_telegram_id):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute("SELECT survey_drinks FROM Users WHERE telegram_id = ?", (input_telegram_id,))
    result = cursor.fetchone()
    connection.close()
    return result[0]


# Метод поиска уже учтенных вкусов напитков по акции "опрос"
def find_survey_tastes(input_telegram_id):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute("SELECT survey_drink_tastes FROM Users WHERE telegram_id = ?", (input_telegram_id,))
    result = cursor.fetchone()
    connection.close()
    return result[0]


# Метод поиска уже учтенных сиропов по акции "опрос"
def find_survey_syrups(input_telegram_id):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute("SELECT survey_syrups FROM Users WHERE telegram_id = ?", (input_telegram_id,))
    result = cursor.fetchone()
    connection.close()
    return result[0]


# Метод поиска пользователя в системе
def find_user(input_telegram_id):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute("SELECT telegram_id FROM Users WHERE telegram_id = ?", (input_telegram_id,))
    result = cursor.fetchone()
    connection.close()
    if result is None:
        return None
    else:
        return result[0]


# Метод поиска пользователей с балансом больше минимальной цены
def find_users(min_price):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute("SELECT telegram_id, balance FROM Users")
    result = cursor.fetchall()
    connection.close()
    ids = []
    for i in result:
        if i[1] >= min_price:
            ids.append(i)
    return ids


# Функция обновления опции cashback
def update_cashback(telegram_id, value):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE Users SET cashback = ? WHERE telegram_id = ?', (value, telegram_id))
    connection.commit()
    connection.close()


# Функция обновления опции survey
def update_survey(telegram_id, value):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE Users SET survey = ? WHERE telegram_id = ?', (value, telegram_id))
    connection.commit()
    connection.close()


# Функция обновления опции cashback
def update_balance(telegram_id, value):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE Users SET balance = ? WHERE telegram_id = ?', (value, telegram_id))
    connection.commit()
    connection.close()


# Функция обновления текущего места пользователя
def update_current_place(telegram_id, value):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE Users SET current_place = ? WHERE telegram_id = ?', (value, telegram_id))
    connection.commit()
    connection.close()


# Функция обновления напитков по акции "опрос"
def update_survey_drinks(telegram_id, values):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    drinks_string = ' '.join(values)
    cursor.execute('UPDATE Users SET survey_drinks = ? WHERE telegram_id = ?', (drinks_string, telegram_id))
    connection.commit()
    connection.close()


# Функция обновления сиропов по акции "опрос"
def update_survey_syrups(telegram_id, values):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    syrups_string = ' '.join(values)
    cursor.execute('UPDATE Users SET survey_syrups = ? WHERE telegram_id = ?', (syrups_string, telegram_id))
    connection.commit()
    connection.close()


# Функция обновления вкусов напитков по акции "опрос"
def update_survey_tastes(telegram_id, values):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    tastes_string = ' '.join(values)
    cursor.execute('UPDATE Users SET survey_drink_tastes = ? WHERE telegram_id = ?', (tastes_string, telegram_id))
    connection.commit()
    connection.close()


# Функция обновления отзыва по акции "опрос"
def update_survey_review(telegram_id, value):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE Users SET survey_review = ? WHERE telegram_id = ?', (value, telegram_id))
    connection.commit()
    connection.close()


# Функция конвертации таблицы SQL в формат Excel
def sql_to_excel():
    connection = sqlite3.connect('users.db')
    df = pd.read_sql('SELECT * FROM Users', connection)
    df.to_excel(r'users.xlsx', index=False)


if __name__ == '__main__':
    init()
    init_counted_drinks()

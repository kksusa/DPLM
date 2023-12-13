"""Основной модуль Telegram-бота"""

import logging
import os
import threading
from time import sleep

import telebot
import schedule

import bonuses
# Функция логирования сообщений между пользователем и ботом в файлы .txt
from chat_logger import chat_logging as cl
import json_handler
import name_convertation
import sqlite
import text_reader
import vendoscope
from buttons import *
from sqlite import *
import phrases

# Стандартный процент скидки в рамках акции "кэшбек"
CASHBACK_DEFAULT = 0.2
# Минимальная стоимость напитка по всей сети
MIN_PRICE = 89

API_TOKEN = json_handler.json_load("json/config.json")["tkn"]
bot = telebot.TeleBot(API_TOKEN)

logging.basicConfig(level=logging.INFO, filename="log.txt", filemode="a",
                    format="%(asctime)s %(levelname)s %(message)s")


# Общая функция системы
def main():
    # Функция, кнопки "кэшбек"
    def cashback(message):
        current_user_id = message.chat.id
        cl(current_user_id, message.text)
        # Поиск параметров пользователя в БД
        current_cashback = find_cashback(current_user_id)
        current_balance = find_balance(current_user_id)
        # Условия проверки пользования акцией "кэшбек"
        if current_cashback == 0:
            current_balance += 100
            update_cashback(current_user_id, 1)
            update_balance(current_user_id, current_balance)
            cashback_text_before = text_reader.read_text("txt/cashback_text_before.txt")
            spend_bonuses = phrases.spend_bonuses(current_balance)
            cashback_text_after = text_reader.read_text("txt/cashback_text_after.txt")
            bot.send_message(current_user_id, cashback_text_before)
            cl(current_user_id, cashback_text_before, True)
            bot.send_message(current_user_id, spend_bonuses)
            cl(current_user_id, spend_bonuses, True)
            bot.send_message(current_user_id, cashback_text_after)
            cl(current_user_id, cashback_text_after, True)
        else:
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(yes_btn, no_btn)
            want_to_deposit = text_reader.read_text("txt/want_to_deposit.txt")
            bot.send_message(current_user_id, want_to_deposit, reply_markup=markup)
            cl(current_user_id, want_to_deposit, True)

    # Функция, кнопки "баланс"
    def balance(message):
        current_user_id = message.chat.id
        cl(current_user_id, message.text)
        current_balance = find_balance(current_user_id)
        spend_bonuses = phrases.spend_bonuses(current_balance)
        bot.send_message(current_user_id, spend_bonuses)
        cl(current_user_id, spend_bonuses, True)

    # Метод проверки участия в акции "опрос"
    def check_survey(message):
        current_user_id = message.chat.id
        current_survey = find_survey(current_user_id)
        return current_survey

    # Функция вывода кнопок по акции "акции"
    def stock(message):
        current_user_id = message.chat.id
        cl(current_user_id, message.text)
        markup_stock = types.InlineKeyboardMarkup(row_width=1)
        markup_stock.add(gorky_stock, sova_stock)
        choose_stock_place = text_reader.read_text("txt/choose_stock_place.txt")
        bot.send_message(current_user_id, choose_stock_place, reply_markup=markup_stock)
        cl(current_user_id, choose_stock_place, True)

    # Функция-напоминание о возможности потратить баланс
    def reminder():
        # Поиск ID пользователей с балансом больше минимальной цены
        current_ids = find_users(MIN_PRICE)
        for i in current_ids:
            try:
                reminder_text = text_reader.read_text("txt/reminder.txt")
                balance_text = phrases.spend_bonuses(i[1])
                bot.send_message(i[0], reminder_text)
                cl(i, reminder_text, True)
                bot.send_message(i[0], balance_text)
                cl(i, balance_text, True)
            except telebot.apihelper.ApiTelegramException as e:
                logging.error(str(e) + f" BLOCKING ID: {i[0]}\n")
                continue

    # Функция-планировщик задач
    def scheduler():
        schedule.every().friday.at("09:00").do(reminder)
        schedule.every().day.at("08:00").do(sqlite.sql_to_excel)
        schedule.every().day.at("09:00").do(sqlite.sql_to_excel)
        schedule.every().day.at("10:00").do(sqlite.sql_to_excel)
        schedule.every().day.at("11:00").do(sqlite.sql_to_excel)
        schedule.every().day.at("12:00").do(sqlite.sql_to_excel)
        schedule.every().day.at("13:00").do(sqlite.sql_to_excel)
        schedule.every().day.at("14:00").do(sqlite.sql_to_excel)
        schedule.every().day.at("15:00").do(sqlite.sql_to_excel)
        schedule.every().day.at("16:00").do(sqlite.sql_to_excel)
        schedule.every().day.at("17:00").do(sqlite.sql_to_excel)
        schedule.every().day.at("18:00").do(sqlite.sql_to_excel)
        schedule.every().day.at("19:00").do(sqlite.sql_to_excel)
        schedule.every().day.at("20:00").do(sqlite.sql_to_excel)
        schedule.every().day.at("21:00").do(sqlite.sql_to_excel)
        schedule.every().day.at("22:00").do(sqlite.sql_to_excel)
        schedule.every().day.at("23:00").do(sqlite.sql_to_excel)
        schedule.every().day.at("00:00").do(sqlite.delete_drinks_table)
        while True:
            schedule.run_pending()
    # Запуск планировщика в отдельном потоке
    t1 = threading.Thread(target=scheduler, daemon=True)
    t1.start()

    # Функция-контроллер выдачи напитка
    def out(data, message):
        try:
            # Напиток для выдачи
            drinkout_drink = data
            current_user_id = message.chat.id
            cl(current_user_id, drinkout_drink)
            # Поиск параметров пользователя в БД
            current_balance = find_balance(current_user_id)
            current_drinkout_place = find_current_place(current_user_id)
            # Проверка возможности выдачи напитка по балансу
            drinkout_ability = bonuses.check_drink_out_ability(data, current_balance)
            if drinkout_ability:
                great_choose = text_reader.read_text("txt/great_choose.txt")
                bot.send_message(current_user_id, great_choose)
                cl(current_user_id, great_choose, True)
                # Выдача напитка
                vendoscope.drink_is_out(current_drinkout_place, drinkout_drink)
                # Вычисление баланса
                current_balance = bonuses.drink_out_calculation(drinkout_drink, current_balance, current_drinkout_place)
                update_balance(current_user_id, current_balance)
                spend_bonuses = phrases.spend_bonuses(current_balance)
                bot.send_message(current_user_id, spend_bonuses)
                cl(current_user_id, spend_bonuses, True)
            else:
                not_enough_bonuses = text_reader.read_text("txt/not_enough_bonuses.txt")
                bot.send_message(current_user_id, not_enough_bonuses)
                cl(current_user_id, not_enough_bonuses, True)
        except:
            something_wrong(message)

    # Функция отображения акций по кофейне
    def stock_out(message, place):
        current_user_id = message.chat.id
        cl(current_user_id, place)
        # Преобразование места для передачи в качестве переменной
        current_place = name_convertation.convertation(place)
        # Чтение описаний к акциям
        stock_phrases = json_handler.json_load(f"json/stock_{current_place}.json")
        pictures_list = []
        # Чтение абсолютных путей изображений
        for dirpath, dirnames, filenames in os.walk(f"{os.getcwd()}/pictures/{current_place}/"):
            for filename in filenames:
                pictures_list.append(os.path.join(dirpath, filename))
        # Отображение акций
        for i in range(len(stock_phrases)):
            bot.send_photo(current_user_id, open(pictures_list[i], 'rb'), stock_phrases[i])
            cl(current_user_id, f"[photo] {stock_phrases[i]}", True)
            sleep(2)

    # Функция "что-то пошло не так :-("
    def something_wrong(message):
        current_user_id = message.chat.id
        something_wrong_text = text_reader.read_text("txt/something_wrong.txt")
        bot.send_message(current_user_id, something_wrong_text)
        cl(current_user_id, something_wrong_text, True)

    # Функция отображения контактов техподдержки
    def support(message):
        current_user_id = message.chat.id
        cl(current_user_id, message.text)
        support_contacts = text_reader.read_text("txt/support_contacts.txt")
        bot.send_message(current_user_id, support_contacts)
        cl(current_user_id, support_contacts, True)

    # Функция-контроллер наличия купленного напитка в системе
    def standard(data, message):
        try:
            # Напиток для проверки на наличие в сервисе "vendoscope.pro"
            current_drink = data
            current_user_id = message.chat.id
            cl(current_user_id, current_drink)
            # Поиск параметров пользователя в БД
            current_balance = find_balance(current_user_id)
            current_place = find_current_place(current_user_id)
            everything_is_ok = text_reader.read_text("txt/everything_is_ok.txt")
            bot.send_message(current_user_id, everything_is_ok)
            cl(current_user_id, everything_is_ok, True)
            # Проверка покупки напитка в сервисе "vendoscope.pro"
            purchase_check = vendoscope.check_bought_drink(data, current_place)
            if purchase_check:
                # Начисление бонусов
                current_balance = bonuses.drink_bonuses_calculation(data, current_balance, current_place,
                                                                    CASHBACK_DEFAULT)
                update_balance(current_user_id, current_balance)
                deposit_bonuses = phrases.deposit_bonuses(current_balance)
                bot.send_message(current_user_id, deposit_bonuses)
                cl(current_user_id, deposit_bonuses, True)
            else:
                no_drink_in_vendoscope = text_reader.read_text("txt/no_drink_in_vendoscope.txt")
                bot.send_message(current_user_id, no_drink_in_vendoscope)
                cl(current_user_id, no_drink_in_vendoscope, True)
                support_text = text_reader.read_text("txt/support.txt")
                bot.send_message(current_user_id, support_text)
                cl(current_user_id, support_text, True)
        except:
            something_wrong(message)

    # Функция отображения кнопок мест по акции "хочу напиток"
    def want_drink_where_you_are(message):
        current_user_id = message.chat.id
        cl(current_user_id, message.text)
        markup_places = types.InlineKeyboardMarkup(row_width=1)
        markup_places.add(gorky_drinkout, sova_drinkout)
        where_you_are = text_reader.read_text("txt/where_you_are.txt")
        bot.send_message(current_user_id, where_you_are, reply_markup=markup_places)
        cl(current_user_id, where_you_are, True)

    # Функция отображения кнопок напитков по акции "хочу напиток"
    def want_drink_what_drink(message):
        current_user_id = message.chat.id
        markup_drinks = types.InlineKeyboardMarkup(row_width=1)
        markup_drinks.add(latte_out, americano_out, chocolate_out, mocaccino_out,
                          capuccino_out, nut_raph_out, chocolate_milk_out, nut_moca_out, nut_moca_milk_out,
                          americano_milk_out, flat_white_out)
        what_drink_wish = text_reader.read_text("txt/what_drink_wish.txt")
        bot.send_message(current_user_id, what_drink_wish, reply_markup=markup_drinks)
        cl(current_user_id, what_drink_wish, True)

    # Функция приветствия по акции "опрос"
    def survey_common(message):
        current_user_id = message.chat.id
        cl(current_user_id, message.text)
        # Проверка на участие в акции "опрос" ранее
        if check_survey(message) == 0:
            markup_survey = types.InlineKeyboardMarkup(row_width=1)
            markup_survey.add(survey_yes)
            survey_common_text = text_reader.read_text("txt/survey_common.txt")
            bot.send_message(current_user_id, survey_common_text, reply_markup=markup_survey)
            cl(current_user_id, survey_common_text, True)
        else:
            no_survey = text_reader.read_text("txt/no_survey.txt")
            bot.send_message(current_user_id, no_survey)
            cl(current_user_id, no_survey, True)

    # Функция с кнопками выбора любимых или желаемых напитков по акции "опрос"
    def survey_drinks(message):
        current_user_id = message.chat.id
        markup_survey_drinks = types.InlineKeyboardMarkup(row_width=1)
        markup_survey_drinks.add(latte_drink, americano_drink, chocolate_drink,
                                 mocaccino_drink, capuccino_drink, nut_raph_drink,
                                 chocolate_milk_drink, nut_moca_drink, nut_moca_milk_drink,
                                 americano_milk_drink, flat_white_drink, survey_drinks_next)
        survey_drinks_text = text_reader.read_text("txt/survey_drinks.txt")
        bot.send_message(current_user_id, survey_drinks_text, reply_markup=markup_survey_drinks)
        cl(current_user_id, survey_drinks_text, True)

    # Функция с кнопками выбора любимых или желаемых сиропов по акции "опрос"
    def survey_syrups(message):
        current_user_id = message.chat.id
        markup_survey_syrups = types.InlineKeyboardMarkup(row_width=1)
        markup_survey_syrups.add(banana_syrup, coconut_syrup, caramel_syrup, nut_syrup, pistachios_syrup,
                                 chocolate_syrup, vanilla_syrup, survey_syrups_next)
        survey_syrups_text = text_reader.read_text("txt/survey_syrups.txt")
        bot.send_message(current_user_id, survey_syrups_text, reply_markup=markup_survey_syrups)
        cl(current_user_id, survey_syrups_text, True)

    # Функция с кнопками выбора желаемых вкусов напитков по акции "опрос"
    def survey_tastes(message):
        current_user_id = message.chat.id
        markup_survey_tastes = types.InlineKeyboardMarkup(row_width=1)
        markup_survey_tastes.add(banana_taste, caramel_taste, ireland_milk_taste, coconut_taste, orange_taste,
                                 french_vanilla_taste, vanilla_taste, apple_pie_taste, raspberry_ice_cream_taste,
                                 cheese_cracker_taste, salt_pistachios_taste, survey_tastes_next)
        survey_drink_tastes = text_reader.read_text("txt/survey_drink_tastes.txt")
        bot.send_message(current_user_id, survey_drink_tastes, reply_markup=markup_survey_tastes)
        cl(current_user_id, survey_drink_tastes, True)

    # Функция для написания отзыва по акции "опрос"
    def survey_review(message):
        current_user_id = message.chat.id
        survey_review_text = text_reader.read_text("txt/survey_review.txt")
        bot.send_message(current_user_id, survey_review_text)
        cl(current_user_id, survey_review_text, True)
        bot.register_next_step_handler(message, survey_finish)

    # Функция начисления бонусов по акции "опрос"
    def survey_finish(message):
        current_user_id = message.chat.id
        current_balance = find_balance(current_user_id)
        current_balance += 50
        update_balance(current_user_id, current_balance)
        update_survey_review(current_user_id, message.text)
        update_survey(current_user_id, 1)
        thanks_for_survey = phrases.thanks_for_survey(current_balance)
        bot.send_message(current_user_id, thanks_for_survey)
        cl(current_user_id, thanks_for_survey, True)

    # Обработчик бота, отвечающий за команду "/start"
    @bot.message_handler(commands=['start'])
    # Функция приветствия и регистрации пользователя в системе
    def greetings(message):
        current_user_id = message.chat.id
        cl(current_user_id, message.text)
        # Поиск пользователя в БД
        found_user = find_user(current_user_id)
        if found_user is None:
            current_username = message.from_user.username
            current_first_name = message.from_user.first_name
            add_user((current_user_id, current_username, current_first_name, 0, 0, 0))
        else:
            current_first_name = message.from_user.first_name
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        markup.add(want_drink_btn, cashback_btn, stock_btn, balance_btn, survey_btn, support_btn)
        greetings_text = phrases.greetings(current_first_name)
        bot.send_message(current_user_id, greetings_text, reply_markup=markup)
        cl(message.chat.id, greetings_text, True)

    # Обработчик бота, отвечающий за текстовые сообщения
    @bot.message_handler(content_types=['text'])
    # Функция, отвечающая за командные или любые другие текстовые сообщения боту
    def any_messages(message):
        if message.text.lower() == "кэшбек":
            cashback(message)
        elif message.text.lower() == "акции":
            stock(message)
        elif message.text.lower() == "баланс":
            balance(message)
        elif message.text.lower() == "техподдержка":
            support(message)
        elif message.text.lower() == "хочу напиток":
            want_drink_where_you_are(message)
        elif message.text.lower() == "опрос":
            survey_common(message)
        else:
            current_user_id = message.chat.id
            cl(current_user_id, message.text)
            dont_know = phrases.dont_know_phrases()
            bot.send_message(message.chat.id, dont_know)
            cl(message.chat.id, dont_know, True)

    # Обработчик бота, отвечающий за callback-кнопки
    @bot.callback_query_handler(func=lambda callback: callback.data)
    # Функция обработки разных callback-запросов
    def check_callback_data(callback):
        # Callback-запрос с выбором купленного напитка
        if callback.data.endswith("_place"):
            current_place = name_convertation.convertation(callback.data)
            current_user_id = callback.message.chat.id
            cl(current_user_id, callback.data)
            update_current_place(current_user_id, current_place)
            markup_drinks = types.InlineKeyboardMarkup(row_width=1)
            markup_drinks.add(latte_btn, americano_btn, chocolate_btn, mocaccino_btn,
                              capuccino_btn, nut_raph_btn, chocolate_milk_btn, nut_moca_btn, nut_moca_milk_btn,
                              americano_milk_btn, flat_white_btn)
            choose_bought_drink = text_reader.read_text("txt/choose_bought_drink.txt")
            bot.send_message(current_user_id, choose_bought_drink, reply_markup=markup_drinks)
            cl(current_user_id, choose_bought_drink, True)
        # Callback-запрос с ответом "да" на акцию "кэшбек"
        elif callback.data == "yes":
            current_user_id = callback.message.chat.id
            cl(current_user_id, callback.data)
            markup_places = types.InlineKeyboardMarkup(row_width=1)
            markup_places.add(gorky_btn, sova_btn)
            where_you_are = text_reader.read_text("txt/where_you_are.txt")
            bot.send_message(current_user_id, where_you_are, reply_markup=markup_places)
            cl(current_user_id, where_you_are, True)
            # Callback-запрос с ответом "нет" на акцию "кэшбек"
        elif callback.data == "no":
            current_user_id = callback.message.chat.id
            cl(current_user_id, callback.data)
            see_you_soon = text_reader.read_text("txt/see_you_soon.txt")
            bot.send_message(current_user_id, see_you_soon)
            cl(current_user_id, see_you_soon, True)
        # Callback-запрос на проверку купленного напитка
        elif callback.data.endswith("_standard"):
            t2 = threading.Thread(target=standard, args=(callback.data, callback.message,))
            t2.start()
        # Callback-запрос на отображение акций выбранного места
        elif callback.data.endswith("_stock"):
            t3 = threading.Thread(target=stock_out, args=(callback.message, callback.data,))
            t3.start()
        # Callback-запрос на отображение кнопок напитков по акции "хочу напиток"
        elif callback.data.endswith("_drinkout"):
            drinkout_place = callback.data
            drinkout_place = name_convertation.convertation(drinkout_place)
            current_user_id = callback.message.chat.id
            cl(current_user_id, drinkout_place)
            update_current_place(current_user_id, drinkout_place)
            want_drink_what_drink(callback.message)
        # Callback-запрос на выдачу напитка по акции "хочу напиток"
        elif callback.data.endswith("_out"):
            t4 = threading.Thread(target=out, args=(callback.data, callback.message,))
            t4.start()
        # Callback-запрос на первый вопрос по акции "опрос"
        elif callback.data == "survey_yes":
            current_user_id = callback.message.chat.id
            cl(current_user_id, callback.data)
            # Проверка на участие в акции "опрос" ранее
            if check_survey(callback.message) == 0:
                survey_drinks(callback.message)
            else:
                no_survey = text_reader.read_text("txt/no_survey.txt")
                bot.send_message(current_user_id, no_survey)
                cl(current_user_id, no_survey, True)
        # Callback-запрос на второй вопрос по акции "опрос"
        elif callback.data == "survey_drinks_next":
            current_user_id = callback.message.chat.id
            cl(current_user_id, callback.data)
            # Проверка на участие в акции "опрос" ранее
            if check_survey(callback.message) == 0:
                survey_syrups(callback.message)
            else:
                no_survey = text_reader.read_text("txt/no_survey.txt")
                bot.send_message(callback.message.chat.id, no_survey)
                cl(current_user_id, no_survey, True)
        # Callback-запрос на третий вопрос по акции "опрос"
        elif callback.data == "survey_syrups_next":
            current_user_id = callback.message.chat.id
            cl(current_user_id, callback.data)
            # Проверка на участие в акции "опрос" ранее
            if check_survey(callback.message) == 0:
                survey_tastes(callback.message)
            else:
                no_survey = text_reader.read_text("txt/no_survey.txt")
                bot.send_message(callback.message.chat.id, no_survey)
                cl(current_user_id, no_survey, True)
        # Callback-запрос на написание отзыва по акции "опрос"
        elif callback.data == "survey_tastes_next":
            current_user_id = callback.message.chat.id
            cl(current_user_id, callback.data)
            # Проверка на участие в акции "опрос" ранее
            if check_survey(callback.message) == 0:
                survey_review(callback.message)
            else:
                no_survey = text_reader.read_text("txt/no_survey.txt")
                bot.send_message(callback.message.chat.id, no_survey)
                cl(current_user_id, no_survey, True)
        # Callback-запрос на обновление напитков в БД по акции "опрос"
        elif callback.data.endswith("_drink"):
            current_user_id = callback.message.chat.id
            current_survey_drinks = find_survey_drinks(current_user_id)
            if current_survey_drinks is None:
                current_survey_drinks = ""
            current_survey_drinks_list = current_survey_drinks.split()
            current_survey_drinks_list.append(callback.data)
            update_survey_drinks(current_user_id, current_survey_drinks_list)
        # Callback-запрос на обновление сиропов в БД по акции "опрос"
        elif callback.data.endswith("_syrup"):
            current_user_id = callback.message.chat.id
            current_survey_syrups = find_survey_syrups(current_user_id)
            if current_survey_syrups is None:
                current_survey_syrups = ""
            current_survey_syrups_list = current_survey_syrups.split()
            current_survey_syrups_list.append(callback.data)
            update_survey_syrups(current_user_id, current_survey_syrups_list)
        # Callback-запрос на обновление вкусов напитков в БД по акции "опрос"
        elif callback.data.endswith("_taste"):
            current_user_id = callback.message.chat.id
            current_survey_tastes = find_survey_tastes(current_user_id)
            if current_survey_tastes is None:
                current_survey_tastes = ""
            current_survey_tastes_list = current_survey_tastes.split()
            current_survey_tastes_list.append(callback.data)
            update_survey_tastes(current_user_id, current_survey_tastes_list)
    # Постоянный опрос сервера Telegram на наличие новых сообщений
    bot.polling()


if __name__ == "__main__":
    main()

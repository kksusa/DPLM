"""Модуль параметрозависмых фраз бота."""

import random

import json_handler


# Метод вывода баланса при списании бонусов
def spend_bonuses(balance):
    if balance % 10 == 1 and balance % 100 != 11:
        return f'Твой баланс: {balance} бонус 😉\nСпасибо, что ты с нами! 🤗'
    elif 2 <= balance % 10 <= 4 and balance // 10 % 10 != 1:
        return f'Твой баланс: {balance} бонуса 😉\nСпасибо, что ты с нами! 🤗'
    else:
        return f'Твой баланс: {balance} бонусов 😉\nСпасибо, что ты с нами! 🤗'


# Метод вывода баланса при начислении бонусов
def deposit_bonuses(balance):
    return f'Отлично👍\n{spend_bonuses(balance)}'


# Метод вывода баланса при списании бонусов после участия в акции "опрос"
def thanks_for_survey(balance):
    return f'Благодарим за участие в опросе😎\n\n{deposit_bonuses(balance)}'


# Метод вывода случайной фразы, если входное сообщение неизвестно
def dont_know_phrases():
    coffee_names = json_handler.json_load("json/coffee_names.json")
    phrases = [
        f"Эммм... Что-то я не могу тебя понять... Пойду-ка бахну {random.choice(coffee_names)}☕️",
        "Мдаааа, похоже на сегодня хорош уже... Надо проспаться. Или, всё-таки, по кофейку? 😎"]
    return random.choice(phrases)


# Метод вывода приветственного сообщения при вводе команды /start
def greetings(first_name):
    return f"""Привееееет, {first_name} ✌️
Очень рад тебе!
Нажми любую кнопку ниже, и мы начнём 😎"""

"""Модуль расчёта бонусов бонусной системы."""

import math
from datetime import datetime
from name_convertation import convertation

import json_handler

# Числа часа начала и окончания "счастливых часов"
HAPPY_HOUR_START_GORKY = 9
HAPPY_HOUR_START_SOVA = 8
HAPPY_HOUR_END_GORKY = 13
HAPPY_HOUR_END_SOVA = 12
# Процент скидки в "счастливые часы"
HAPPY_HOUR_DISCOUNT = 0.1


# Метод начисления бонусов
def drink_bonuses_calculation(drink, balance, place, cashback):
    # Преобразование напитка для передачи в качестве переменной
    drink = convertation(drink)
    current_hour = datetime.now().time().hour
    # Загрузка цен на напитки
    drinks = json_handler.json_load("json/drinks.json")
    if place == "sova":
        if HAPPY_HOUR_START_SOVA <= current_hour < HAPPY_HOUR_END_SOVA:
            balance += math.ceil(round(drinks[drink] * (1 - HAPPY_HOUR_DISCOUNT)) * cashback)
        else:
            balance += math.ceil((drinks[drink] * cashback))
    elif place == "gorky":
        if HAPPY_HOUR_START_GORKY <= current_hour < HAPPY_HOUR_END_GORKY:
            balance += math.ceil(round(drinks[drink] * (1 - HAPPY_HOUR_DISCOUNT)) * cashback)
        else:
            balance += math.ceil(drinks[drink] * cashback)
    return balance


# Метод списания бонусов
def drink_out_calculation(drink, balance, place):
    # Преобразование напитка для передачи в качестве переменной
    drink = convertation(drink)
    current_hour = datetime.now().time().hour
    # Загрузка цен на напитки
    drinks = json_handler.json_load("json/drinks.json")
    if place == "sova":
        if HAPPY_HOUR_START_SOVA <= current_hour < HAPPY_HOUR_END_SOVA:
            balance -= round(drinks[drink] * (1 - HAPPY_HOUR_DISCOUNT))
        else:
            balance -= drinks[drink]
    elif place == "gorky":
        if HAPPY_HOUR_START_GORKY <= current_hour < HAPPY_HOUR_END_GORKY:
            balance -= round(drinks[drink] * (1 - HAPPY_HOUR_DISCOUNT))
        else:
            balance -= drinks[drink]
    return balance


# Метод проверки возможности списания бонусов
def check_drink_out_ability(drink, balance):
    # Преобразование напитка для передачи в качестве переменной
    drink = convertation(drink)
    # Загрузка цен на напитки
    drinks = json_handler.json_load("json/drinks.json")
    if balance >= drinks[drink]:
        return True
    else:
        return False

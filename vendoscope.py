"""Модуль взаимодействия с сервисом vendoscope.pro"""

import logging
import time
from datetime import datetime, timedelta

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

import json_handler
import sqlite
from name_convertation import convertation

# Первая и последняя минуты для проверки наличия напитка по акции "кэшбек"
FIRST_MINUTE = 1
LAST_MINUTE = 5
# Первый и последний напитки в списке для проверки наличия напитка по акции "кэшбек"
FIRST_SEARCH = 1
LAST_SEARCH = 5

# Опции браузера
o = Options()
# o.add_experimental_option("detach", True)
o.add_argument("--headless")
o.add_argument("--no-sandbox")

# Параметр расположения движка chromedriver в системе linux
# service = Service(executable_path='/root/downloads/chromedriver')

logging.basicConfig(level=logging.INFO, filename="log.txt", filemode="a",
                    format="%(asctime)s %(levelname)s %(message)s")


# Функция для входа в сервис vendoscope.pro
def login():
    lgn = json_handler.json_load("json/config.json")["lgn"]
    pswd = json_handler.json_load("json/config.json")["pswd"]
    global driver
    driver = webdriver.Chrome(options=o)
    driver.get("https://vendoscope.pro/login")
    try:
        username = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located((By.XPATH, "//input[@id='input-login-email']"))
        )
    except Exception as e:
        logging.error(str(e) + f"\n")
        driver.close()
    finally:
        username.send_keys(lgn)
        user_submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        user_submit_button.click()
    try:
        password = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located((By.XPATH, "//input[@id='input-login-password']"))
        )
    except Exception as e:
        logging.error(str(e) + f"\n")
        driver.close()
    finally:
        password.send_keys(pswd)
        password_submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        password_submit_button.click()


# Функция выдачи напитка в сервисе vendoscope.pro
def drink_is_out(place, requested_drink):
    login()
    # Загрузка транслитераций напитков
    drinks = json_handler.json_load("json/drinks_transliteration.json")
    # Преобразование напитка для передачи в качестве переменной
    requested_drink = convertation(requested_drink)
    # Транслитерация напитка
    requested_drink = drinks[requested_drink]
    # Загрузка напитков
    vendoscope_drinks = json_handler.json_load("json/vendoscope_drinks.json")
    time.sleep(2)
    # Переход на страницу управления кофемашиной
    if place == "gorky":
        driver.get("https://vendoscope.pro/machines/88b7fbbb-0f22-4170-ba89-d03fa0ca7837")
    elif place == "sova":
        driver.get("https://vendoscope.pro/machines/ba62c75d-9e57-4553-9833-1e8bcd4a622c")
    try:
        prod_out_button = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located((By.CLASS_NAME, 'ml-2'))
        )
    except Exception as e:
        logging.error(str(e) + f"\n")
        driver.close()
    finally:
        prod_out_button.click()
    try:
        select_prod_button = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located((By.CLASS_NAME, "multiselect__single"))
        )
    except Exception as e:
        logging.error(str(e) + f"\n")
        driver.close()
    finally:
        select_prod_button.click()
    try:
        WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located((By.CLASS_NAME, "multiselect__content")))
    except Exception as e:
        logging.error(str(e) + f"\n")
        driver.close()
    finally:
        drinks_out = driver.find_elements(By.CLASS_NAME, "multiselect__element")
        for i in range(len(vendoscope_drinks)):
            if requested_drink == vendoscope_drinks[i]:
                drinks_out[i].click()
                break
    # Часть кода закомментирована, т.к. отвечает за реальную выдачу напитка
    # try:
    #     prod_is_out_button = WebDriverWait(driver, 10).until(
    #         expected_conditions.presence_of_element_located((By.CLASS_NAME, "btn-primary")))
    # except Exception as e:
    #     logging.error(str(e) + f"\n")
    #     driver.close()
    # finally:
    #     prod_is_out_button.click()
    driver.close()


def check_bought_drink(drink, place):
    # Часть кода закомментирована, для быстрой демонстрации работы кода
    # time.sleep(300)
    # Преобразование напитка для передачи в качестве переменной
    drink = convertation(drink)
    # Загрузка напитков и мест
    drinks = json_handler.json_load("json/drinks_transliteration.json")
    places = json_handler.json_load("json/places_transliteration.json")
    # Транслитерация напитка и места
    drink_trans = drinks[drink]
    place_trans = places[place]
    check_time = []
    current_time = datetime.now()
    # Поиск напитка по временному интервалу в таблице Counted_drinks
    for i in range(FIRST_MINUTE, LAST_MINUTE + 1):
        check_time.append(
            ((current_time - timedelta(minutes=i - 1)).hour, (current_time - timedelta(minutes=i - 1)).minute))
    check_time.reverse()
    for i in check_time:
        result = sqlite.find_drinks(place_trans, drink_trans, i[0], i[1])
        if len(result) != 0:
            return False
    login()
    time.sleep(2)
    # Переход на страницу с таблицей чеков с напитками
    driver.get("https://vendoscope.pro/receipts")
    suitable_drinks = []
    try:
        WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located((By.XPATH, f'//table/tbody/tr[5]/td[5]'))
        )
    except Exception as e:
        logging.error(str(e) + f"\n")
        driver.close()
    finally:
        # Поиск напитка по количественному интервалу в таблице чеков
        for i in range(FIRST_SEARCH, LAST_SEARCH + 1):
            # Извлечение данных о кофемашине
            current_machine = driver.find_element(By.XPATH, f'//table/tbody/tr[{i}]/td[1]').text
            # Извлечение данных о напитке
            current_drink = driver.find_element(By.XPATH, f'//table/tbody/tr[{i}]/td[3]').text.lower()
            # Проверка на соответствие напитка и кофемашины
            if current_machine == place_trans and current_drink == drink_trans:
                # Извлечение данных о времени покупки
                purchase_datetime = driver.find_element(By.XPATH, f'//table/tbody/tr[{i}]/td[5]').text.split()
                purchase_time = purchase_datetime[1].split(":")
                purchase_hour = int(purchase_time[0])
                purchase_minute = int(purchase_time[1])
                suitable_drinks.append(
                    (current_machine, current_drink, purchase_hour, purchase_minute))
    if not suitable_drinks:
        driver.close()
        return False
    else:
        for i in suitable_drinks:
            for j in check_time:
                if j[0] == i[2] and j[1] == i[3]:
                    # Если напиток найден, добавляем его в таблицу Counted_drinks
                    sqlite.add_drink(i)
                    driver.close()
                    return True
        driver.close()
        return False

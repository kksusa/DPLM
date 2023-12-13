"""Модуль загрузки json-файла."""

import json


# Функция загрузки
def json_load(json_path):
    with open(json_path, encoding='utf-8') as file:
        json_file = json.load(file)
    return json_file

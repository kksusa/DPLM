"""Модуль конвертации входящего параметра для передачи в качестве переменной."""


# Функция конвертации
def convertation(name):
    last_symbol = name.rfind("_")
    return name[:last_symbol]

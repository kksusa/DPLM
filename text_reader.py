"""Модуль чтения текстовых файлов."""


# Функция чтения текстовых файлов
def read_text(file_path):
    with open(file_path, "r", encoding='utf-8') as file:
        result_line = ""
        while True:
            line = file.readline()
            if not line:
                break
            result_line += line
        return result_line

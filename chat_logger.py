"""Модуль логирования чата между пользователем и ботом."""

import datetime


# Функция логирования
def chat_logging(user_id, text, bot=False):
    current_time = datetime.datetime.now()
    with open(f"users/{user_id}.txt", "a", encoding='utf-8') as file:
        if bot is False:
            file.writelines("(USER) " + str(current_time) + " ")
            file.writelines(text + "\n")
        else:
            file.writelines("(BOT) " + str(current_time) + " ")
            file.writelines(text + "\n\n")

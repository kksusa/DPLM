"""Модуль запуска бота."""

import bot_controller

while True:
    try:
        bot_controller.main()
    except:
        continue

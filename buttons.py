"""Модуль с кнопками клавиатур."""

from telebot import types

# Кнопки основной клавиатуры ReplyKeyboard
cashback_btn = types.KeyboardButton("КЭШБЕК")
stock_btn = types.KeyboardButton("АКЦИИ")
balance_btn = types.KeyboardButton("БАЛАНС")
want_drink_btn = types.KeyboardButton("ХОЧУ НАПИТОК")
support_btn = types.KeyboardButton("ТЕХПОДДЕРЖКА")
survey_btn = types.KeyboardButton("ОПРОС")

# Кнопки клавиатур InlineKeyboard
# Кнопки для зачисления бонусов по акции "кэшбек"
yes_btn = types.InlineKeyboardButton(text="ДА", callback_data="yes")
no_btn = types.InlineKeyboardButton(text="НЕТ", callback_data="no")

# Кнопка для подтверждения участия в акции "опрос"
survey_yes = types.InlineKeyboardButton(text="ПОГНАЛИ!", callback_data="survey_yes")

# Суффиксы:
# _standard - начисление бонусов по напитку
# _out - выдача напитка
# _drink - уче напитка по акции "опрос"
# Кнопки на напиток "латте"
latte_btn = types.InlineKeyboardButton(text="ЛАТТЕ", callback_data="latte_standard")
latte_out = types.InlineKeyboardButton(text="ЛАТТЕ", callback_data="latte_out")
latte_drink = types.InlineKeyboardButton(text="ЛАТТЕ", callback_data="latte_drink")

# Кнопки на напиток "американо"
americano_btn = types.InlineKeyboardButton(text="АМЕРИКАНО", callback_data="americano_standard")
americano_out = types.InlineKeyboardButton(text="АМЕРИКАНО", callback_data="americano_out")
americano_drink = types.InlineKeyboardButton(text="АМЕРИКАНО", callback_data="americano_drink")

# Кнопки на напиток "американо со сливками"
americano_milk_btn = types.InlineKeyboardButton(text="АМЕРИКАНО СО СЛИВКАМИ", callback_data="americano_milk_standard")
americano_milk_out = types.InlineKeyboardButton(text="АМЕРИКАНО СО СЛИВКАМИ", callback_data="americano_milk_out")
americano_milk_drink = types.InlineKeyboardButton(text="АМЕРИКАНО СО СЛИВКАМИ", callback_data="americano_milk_drink")

# Кнопки на напиток "капучино"
capuccino_btn = types.InlineKeyboardButton(text="КАПУЧИНО", callback_data="capuccino_standard")
capuccino_out = types.InlineKeyboardButton(text="КАПУЧИНО", callback_data="capuccino_out")
capuccino_drink = types.InlineKeyboardButton(text="КАПУЧИНО", callback_data="capuccino_drink")

# Кнопки на напиток "флэт уайт"
flat_white_btn = types.InlineKeyboardButton(text="ФЛЭТ УАЙТ", callback_data="flat_white_standard")
flat_white_out = types.InlineKeyboardButton(text="ФЛЭТ УАЙТ", callback_data="flat_white_out")
flat_white_drink = types.InlineKeyboardButton(text="ФЛЭТ УАЙТ", callback_data="flat_white_drink")

# Кнопки на напиток "мокачино"
mocaccino_btn = types.InlineKeyboardButton(text="МОКАЧИНО", callback_data="mocaccino_standard")
mocaccino_out = types.InlineKeyboardButton(text="МОКАЧИНО", callback_data="mocaccino_out")
mocaccino_drink = types.InlineKeyboardButton(text="МОКАЧИНО", callback_data="mocaccino_drink")

# Кнопки на напиток "ореховый раф"
nut_raph_btn = types.InlineKeyboardButton(text="ОРЕХОВЫЙ РАФ", callback_data="nut_raph_standard")
nut_raph_out = types.InlineKeyboardButton(text="ОРЕХОВЫЙ РАФ", callback_data="nut_raph_out")
nut_raph_drink = types.InlineKeyboardButton(text="ОРЕХОВЫЙ РАФ", callback_data="nut_raph_drink")

# Кнопки на напиток "ореховый мокко"
nut_moca_btn = types.InlineKeyboardButton(text="ОРЕХОВЫЙ МОККО", callback_data="nut_moca_standard")
nut_moca_out = types.InlineKeyboardButton(text="ОРЕХОВЫЙ МОККО", callback_data="nut_moca_out")
nut_moca_drink = types.InlineKeyboardButton(text="ОРЕХОВЫЙ МОККО", callback_data="nut_moca_drink")

# Кнопки на напиток "ореховый мокко со сливками"
nut_moca_milk_btn = types.InlineKeyboardButton(text="ОРЕХОВЫЙ МОККО СО СЛИВКАМИ", callback_data="nut_moca_milk_standard")
nut_moca_milk_out = types.InlineKeyboardButton(text="ОРЕХОВЫЙ МОККО СО СЛИВКАМИ", callback_data="nut_moca_milk_out")
nut_moca_milk_drink = types.InlineKeyboardButton(text="ОРЕХОВЫЙ МОККО СО СЛИВКАМИ", callback_data="nut_moca_milk_drink")

# Кнопки на напиток "горячий шоколад"
chocolate_btn = types.InlineKeyboardButton(text="ГОРЯЧИЙ ШОКОЛАД", callback_data="chocolate_standard")
chocolate_out = types.InlineKeyboardButton(text="ГОРЯЧИЙ ШОКОЛАД", callback_data="chocolate_out")
chocolate_drink = types.InlineKeyboardButton(text="ГОРЯЧИЙ ШОКОЛАД", callback_data="chocolate_drink")

# Кнопки на напиток "сливочный шоколад"
chocolate_milk_btn = types.InlineKeyboardButton(text="СЛИВОЧНЫЙ ШОКОЛАД", callback_data="chocolate_milk_standard")
chocolate_milk_out = types.InlineKeyboardButton(text="СЛИВОЧНЫЙ ШОКОЛАД", callback_data="chocolate_milk_out")
chocolate_milk_drink = types.InlineKeyboardButton(text="СЛИВОЧНЫЙ ШОКОЛАД", callback_data="chocolate_milk_drink")

# Кнопки на сиропы при участии в акции "опрос"
banana_syrup = types.InlineKeyboardButton(text="БАНАНОВЫЙ", callback_data="banana_syrup")
coconut_syrup = types.InlineKeyboardButton(text="КОКОСОВЫЙ", callback_data="coconut_syrup")
caramel_syrup = types.InlineKeyboardButton(text="КАРАМЕЛЬНЫЙ", callback_data="caramel_syrup")
nut_syrup = types.InlineKeyboardButton(text="ЛЕСНОЙ ОРЕХ", callback_data="nut_syrup")
pistachios_syrup = types.InlineKeyboardButton(text="ФИСТАШКА", callback_data="pistachios_syrup")
chocolate_syrup = types.InlineKeyboardButton(text="ШОКОЛАДНЫЙ", callback_data="chocolate_syrup")
vanilla_syrup = types.InlineKeyboardButton(text="ВАНИЛЬНЫЙ", callback_data="vanilla_syrup")

# Кнопки на вкусы напитков при участии в акции "опрос"
banana_taste = types.InlineKeyboardButton(text="БАНАНОВЫЙ", callback_data="banana_taste")
caramel_taste = types.InlineKeyboardButton(text="КАРАМЕЛЬНЫЙ", callback_data="caramel_taste")
ireland_milk_taste = types.InlineKeyboardButton(text="ИРЛАНДСКИЕ СЛИВКИ", callback_data="ireland_milk_taste")
coconut_taste = types.InlineKeyboardButton(text="КОКОСОВЫЙ", callback_data="coconut_taste")
orange_taste = types.InlineKeyboardButton(text="АПЕЛЬСИНОВЫЙ", callback_data="orange_taste")
french_vanilla_taste = types.InlineKeyboardButton(text="ФРАНЦУЗСКАЯ ВАНИЛЬ", callback_data="french_vanilla_taste")
vanilla_taste = types.InlineKeyboardButton(text="ВАНИЛЬНЫЙ", callback_data="vanilla_taste")
apple_pie_taste = types.InlineKeyboardButton(text="ЯБЛОЧНЫЙ ПИРОГ", callback_data="apple_pie_taste")
raspberry_ice_cream_taste = types.InlineKeyboardButton(text="МАЛИНОВЫЙ ПЛОМБИР", callback_data="raspberry_ice_cream_taste")
cheese_cracker_taste = types.InlineKeyboardButton(text="СЫРНЫЙ КРЕКЕР", callback_data="cheese_cracker_taste")
salt_pistachios_taste = types.InlineKeyboardButton(text="СОЛЁНАЯ ФИСТАШКА", callback_data="salt_pistachios_taste")

# Кнопки мест для начисления бонусов
sova_btn = types.InlineKeyboardButton(text='ФИТНЕС-КЛУБ "СОВА"', callback_data="sova_place")
gorky_btn = types.InlineKeyboardButton(text='ТРК "ГОРКИ"', callback_data="gorky_place")

# Кнопки мест для отображения акций
sova_stock = types.InlineKeyboardButton(text='ФИТНЕС-КЛУБ "СОВА"', callback_data="sova_stock")
gorky_stock = types.InlineKeyboardButton(text='ТРК "ГОРКИ"', callback_data="gorky_stock")

# Кнопки мест для выдачи напитка
sova_drinkout = types.InlineKeyboardButton(text='ФИТНЕС-КЛУБ "СОВА"', callback_data="sova_drinkout")
gorky_drinkout = types.InlineKeyboardButton(text='ТРК "ГОРКИ"', callback_data="gorky_drinkout")

# Кнопки "продолжить" для акции "опрос"
survey_drinks_next = types.InlineKeyboardButton(text='ПРОДОЛЖИТЬ ➡', callback_data="survey_drinks_next")
survey_syrups_next = types.InlineKeyboardButton(text='ПРОДОЛЖИТЬ ➡', callback_data="survey_syrups_next")
survey_tastes_next = types.InlineKeyboardButton(text='ПРОДОЛЖИТЬ ➡', callback_data="survey_tastes_next")

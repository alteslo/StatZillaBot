from aiogram import types


def kb_service_selection(width=1):
    """Клавиатура для основного выбора услуг"""
    buttons = [
        types.InlineKeyboardButton(text="Статистическая обработка данных",
                                   callback_data="stat_proc"),
        types.InlineKeyboardButton(text="Литобзор",
                                   callback_data="lit_rev"),
        types.InlineKeyboardButton(text="Другое",
                                   callback_data="other")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=width)
    keyboard.add(*buttons)
    return keyboard


def kb_stat_processing_choice(width=1):
    """Клавиатура для выбора услуг статистического анализа"""
    buttons = [
            types.InlineKeyboardButton(text="Сбор данных",
                                       callback_data="stat_data_coll"),
            types.InlineKeyboardButton(text="Маркетинговые исследования",
                                       callback_data="stat_market_res"),
            types.InlineKeyboardButton(text="Моделирование и прогнозирование",
                                       callback_data="stat_model"),
            types.InlineKeyboardButton(text="Статистическая обработка",
                                       callback_data="stat_stat_proc"),
            types.InlineKeyboardButton(text="Machine Learning",
                                       callback_data="stat_mach_learn"),
            types.InlineKeyboardButton(text="Создание управленческих панелей",
                                       callback_data="stat_manage_pan"),
            types.InlineKeyboardButton(text="Не нашли подходящий инструмент?",
                                       callback_data="stat_no_one")
        ]
    keyboard = types.InlineKeyboardMarkup(row_width=width)
    keyboard.add(*buttons)
    return keyboard


def kb_price_answer(width=1):
    """Клавиатура для выбора услуг статистического анализа"""
    buttons = [
            types.InlineKeyboardButton(text="Хотите скидку?",
                                       callback_data="want_discount"),
            types.InlineKeyboardButton(text="Вернуться к выбору услуг",
                                       callback_data="back_stat_choice"),
            types.InlineKeyboardButton(text="Вернуться к началу",
                                       callback_data="back_serv_selection")

        ]
    keyboard = types.InlineKeyboardMarkup(row_width=width)
    keyboard.add(*buttons)
    return keyboard

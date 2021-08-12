from aiogram.types import InlineKeyboardMarkup
from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import KeyboardButton

from aiogram.utils.callback_data import CallbackData


def kb_contact():
    """Клавиатура для выбора услуг статистического анализа"""
    buttons = KeyboardButton(text="Поделиться контактом с тех. поддержкой \U0001F4F2",
                             request_contact=True)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(buttons)
    return keyboard

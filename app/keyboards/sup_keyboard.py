import random

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import KeyboardButton

from app.keyboards.callback_datas import support_callback
from app.keyboards.callback_datas import cancel_support_callback
from app.keyboards.callback_datas import back_callback
from app.app_data import support_ids


async def check_support_available(support_id, storage=MemoryStorage()):
    state = await storage.get_state(chat=support_id, user=support_id)

    if state == "in_support":
        return
    else:
        return support_id



async def get_support_manager():
    random.shuffle(support_ids)
    for support_id in support_ids:
        support_id = await check_support_available(support_id)
        if support_id:
            return support_id
        else:
            return


async def kb_support(messages, user_id=None):
    """Клавиатура"""
    if user_id:
        contact_id = int(user_id)
        as_user = "no"
        text = "Ответить пользователю"
        buttons = [
            InlineKeyboardButton(
                    text=text,
                    callback_data=support_callback.new(
                            messages=messages,
                            user_id=contact_id,
                            as_user=as_user
                    )
                )
        ]
    else:
        contact_id = await get_support_manager()
        as_user = "yes"
        if messages == "many" and contact_id is None:
            return False
        elif messages == "one" and contact_id is None:
            contact_id = random.choice(support_ids)

        if messages == "one":
            text = "Написать одно сообщение менеджеру"
            buttons = [
                InlineKeyboardButton(
                        text=text,
                        callback_data=support_callback.new(
                                messages=messages,
                                user_id=contact_id,
                                as_user=as_user
                        )
                    ),
                InlineKeyboardButton(
                    text="Хочу чтобы мне позвонил менеджер",
                    callback_data="share_phone"),
                InlineKeyboardButton(
                        text="Вернуться в начало",
                        callback_data=back_callback.new(
                                deep="start",

                        )
                    )
            ]
        else:
            text = "Написать оператору"
            buttons = [
                InlineKeyboardButton(
                        text=text,
                        callback_data=support_callback.new(
                                messages=messages,
                                user_id=contact_id,
                                as_user=as_user
                        )
                    )]

    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)

    if messages == "many":
        keyboard.add(
            InlineKeyboardButton(
                text="Завершить сеанс",
                callback_data=cancel_support_callback.new(
                    user_id=contact_id
                )
            )
        )
    return keyboard


def cancel_support(user_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Завершить сеанс",
                    callback_data=cancel_support_callback.new(
                        user_id=user_id
                    )
                )
            ]
        ]
    )


async def kb_share_phone():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        KeyboardButton(
            text="Поделись телефоном \U0001F919",
            request_contact=True
        )
    )
    return keyboard

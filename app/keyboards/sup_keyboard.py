import random
import re

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

from app.keyboards.callback_datas import support_callback
from app.keyboards.callback_datas import cancel_support_callback
from app.app_data import support_ids


async def check_support_available(support_id, storage: MemoryStorage):
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
    else:
        contact_id = await get_support_manager()
        as_user = "yes"
        if messages == "many" and contact_id is None:
            return False
        elif messages == "one" and contact_id is None:
            contact_id = random.choice(support_ids)
        if messages == "one":
            text = "Написать одно сообщение в техподдержку"
        else:
            text = "Написать оператору"
        
        keyboard = InlineKeyboardMarkup()
        keyboard.add(
                InlineKeyboardButton(
                    text=text,
                    callback_data=support_callback.new(
                            messages=messages,
                            user_id=contact_id,
                            as_user=as_user
                    )
                )
        )
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

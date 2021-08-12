import keyword
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Text

from app.states.interview import Interview
from app import keyboards
from app.keyboards.callback_datas import help_callback


async def share_contact(call: types.CallbackQuery):
    await call.message.delete()
    await Interview.need_help.set()


async def suppp(message: types.Message):
    keyboard = keyboards.kb_contact()
    await message.answer(text="Труляля поддержка делись телефоном",
                         reply_markup=keyboard)


def register_handlers_Support(dp: Dispatcher):

    dp.register_callback_query_handler(
            share_contact,
            help_callback.filter(),
            state=Interview.waiting_for_stat_processing_choice)
    dp.register_message_handler(suppp, Text(contains=""), state=Interview.need_help)

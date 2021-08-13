from aiogram import Dispatcher, types
from aiogram.dispatcher.storage import FSMContext

from app.states.interview import Interview
from app import keyboards
from app.keyboards.callback_datas import support_callback


async def get_support_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    second_id = data.get("second_id")

    await message(second_id,
                           f"Вам письмо! Вы можете ответить нажав на кнопку ниже")
    keyboard = await support_keyboard(messages="one", user_id=message.from_user.id)
    await message.copy_to(second_id, reply_markup=keyboard)

    await message.answer("Вы отправили это сообщение!")
    await state.reset_state()


async def ask_suport(message: types.Message):
    text = "Хотите написать сообщение техподдержке? Нажмите на кнопку ниже!"
    keyboard = await keyboards.kb_support(messages="one")
    await message.answer(text=text, reply_markup=keyboard)


def register_handlers_Support(dp: Dispatcher):
    dp.register_message_handler(ask_suport, commands="support"),
    dp.register_callback_query_handler(
            share_contact,
            support_callback.filter(messages="one"),
            state=Interview.waiting_for_stat_processing_choice)
    

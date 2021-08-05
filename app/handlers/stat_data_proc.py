from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from app.states.interview import Interview
from app import keyboards
from app import app_data


async def interview_start(message: types.Message, state: FSMContext):
    """Обработчик первого шага, реагирующий на команду start"""
    await state.finish()
    user_name = message.from_user.first_name
    await message.answer(
        f"Приветствую, {user_name}!",
        reply_markup=types.ReplyKeyboardRemove()
    )

    keyboard = keyboards.kb_service_selection()
    await message.answer("Какую услугу вы хотите получить?",
                         reply_markup=keyboard)

    await Interview.waiting_for_service_selection.set()


async def stat_processing_choice(call: types.CallbackQuery, state: FSMContext):
    """Функция вызываемая только из состояния waiting_for_service_selection"""

    await state.update_data(chosen_main_service=call.data)

    keyboard = keyboards.kb_stat_processing_choice(1)
    if call.data == "stat_proc":
        await call.message.edit_text("Теперь выберите вид анализа:",
                                     reply_markup=keyboard)
        await Interview.waiting_for_stat_processing_choice.set()
    else:
        await call.message.answer("пока не написал код")
        await state.finish()
    await call.answer()


async def stat_price_answer(call: types.CallbackQuery, state: FSMContext):
    """
    Функция вызываемая только из состояния waiting_for_stat_processing_choice
    """
    await state.update_data(chosen_stat_processing=call.data)

    keyboard = keyboards.kb_price_answer(1)
    option = app_data.stat_datas[call.data][0]
    bill = app_data.stat_datas[call.data][1]

    await call.message.edit_text(f"Вы выбрали: {option} стоимость составит: \n"
                                 f"<u><b>{bill}</b></u> р.",
                                 parse_mode='HTML',
                                 reply_markup=keyboard)
    await Interview.price_answer.set()
    await call.answer()


async def return_to_stat_processing_choice(call: types.CallbackQuery,
                                           state: FSMContext):
    await state.update_data(chosen_stat_processing="")

    if call.data == "back_stat_choice":
        keyboard = keyboards.kb_stat_processing_choice(1)
        await call.message.edit_text("Выберите вид анализа:",
                                     reply_markup=keyboard)
        await Interview.waiting_for_stat_processing_choice.set()
    elif call.data == "back_serv_selection":
        keyboard = keyboards.kb_service_selection(1)
        await call.message.edit_text("Какую услугу вы хотите получить?",
                                     reply_markup=keyboard)
        await state.finish()
        await Interview.waiting_for_service_selection.set()
    await call.answer()


def register_handlers_Analysis(dp: Dispatcher):

    dp.register_message_handler(interview_start, commands="start", state="*")
    dp.register_callback_query_handler(
        stat_processing_choice,
        text="stat_proc",
        state=Interview.waiting_for_service_selection
        )
    # Регистрируем обработчик на цены
    for data in app_data.stat_datas.keys():
        dp.register_callback_query_handler(
            stat_price_answer,
            text=data,
            state=Interview.waiting_for_stat_processing_choice
        )
    dp.register_callback_query_handler(
        return_to_stat_processing_choice,
        text="back_stat_choice",
        state=Interview.price_answer
        )
    dp.register_callback_query_handler(
        return_to_stat_processing_choice,
        text="back_serv_selection",
        state=Interview.price_answer
        )

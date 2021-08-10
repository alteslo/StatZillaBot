from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from app.states.interview import Interview
from app import keyboards
from app import app_data
from app.keyboards.callback_datas import service_callback
from app.keyboards.callback_datas import stat_callback
from app.keyboards.callback_datas import need_help_callback


async def stat_processing_choice(call: types.CallbackQuery,
                                 callback_data: dict,
                                 state: FSMContext):
    """Функция вызываемая только из состояния waiting_for_service_selection"""
    print(callback_data)
    service_choise = callback_data.get("main_services")
    await state.update_data(chosen_main_service=service_choise)
    user_id = call.from_user.id
    keyboard = keyboards.kb_stat_processing_choice(user_id)
    if service_choise == "stat_proc":
        await call.message.edit_text("Теперь выберите вид анализа:",
                                     reply_markup=keyboard)
        await Interview.waiting_for_stat_processing_choice.set()
    else:
        await call.message.answer("пока не написал код")
        await state.finish()
    await call.answer()


async def stat_price_answer(call: types.CallbackQuery,
                            callback_data: dict,
                            state: FSMContext):
    """
    Функция вызываемая только из состояния waiting_for_stat_processing_choice
    """
    print(callback_data)
    if "help" in callback_data.values():
        await call.message.edit_text(text="Вы выбрали помощь зала",
                                     parse_mode='HTML')
        await Interview.need_help.set()
        await call.answer()
    else:
        choice = callback_data.get(("service"))
        await state.update_data(chosen_stat_processing=choice)

        keyboard = keyboards.kb_price_answer()
        option = app_data.stat_datas[choice][0]
        bill = app_data.stat_datas[choice][1]

        await call.message.edit_text(
                                f"Вы выбрали: {option} стоимость составит:\n"
                                f"<u><b>{bill}</b></u> р.",
                                parse_mode='HTML',
                                reply_markup=keyboard)
        await Interview.price_answer.set()
        await call.answer()


def register_handlers_Analysis(dp: Dispatcher):
    dp.register_callback_query_handler(
        stat_processing_choice,
        service_callback.filter(main_services="stat_proc"),
        state=Interview.waiting_for_service_selection
        )
    dp.register_callback_query_handler(
            stat_price_answer,
            need_help_callback.filter(),
            state=Interview.waiting_for_stat_processing_choice
        )
    # Регистрируем обработчик на цены
    for data in app_data.stat_datas:
        dp.register_callback_query_handler(
            stat_price_answer,
            stat_callback.filter(service=data),
            state=Interview.waiting_for_stat_processing_choice
        )

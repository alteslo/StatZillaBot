
from aiogram import Dispatcher, types
from aiogram.dispatcher.storage import FSMContext

from app.states.interview import Interview
from app.keyboards import keyboards
from app.keyboards.callback_datas import back_callback


async def return_to_stat_processing_choice(call: types.CallbackQuery,
                                           callback_data: dict,
                                           state: FSMContext):
    await state.update_data(chosen_stat_processing="")

    choice = callback_data.get(("deep"))
    if choice == "stat_choice":
        keyboard = keyboards.kb_stat_processing_choice()
        await call.message.edit_text("Выберите вид анализа:",
                                     reply_markup=keyboard)
        await Interview.waiting_for_stat_processing_choice.set()
    elif choice == "start":
        keyboard = keyboards.kb_service_selection(1)
        await call.message.edit_text("Какую услугу вы хотите получить?",
                                     reply_markup=keyboard)
        await state.finish()
        await Interview.waiting_for_service_selection.set()
    await call.answer()


def register_handlers_return(dp: Dispatcher):
    dp.register_callback_query_handler(
            return_to_stat_processing_choice,
            back_callback.filter(),
            state=Interview.price_answer
            )

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from app import keyboards
from app.keyboards.callback_datas import support_callback
from app.keyboards.callback_datas import cancel_support_callback
from app.keyboards.callback_datas import help_callback
from app.utils.db_api.sqlite import db
from app.app_data import support_ids


async def ask_suport_call(call: types.CallbackQuery):
    text = "Хотите связаться с техподдержкой? Нажмите на кнопку ниже!"
    keyboard = await keyboards.kb_support(messages="many")

    if not keyboard:
        await call.message.edit_text("К сожалению, сейчас нет свободных операторов. Попробуйте позже.")
        return
    await call.message.edit_text(text, reply_markup=keyboard)


async def send_to_support_call(call: types.CallbackQuery,
                               state: FSMContext,
                               callback_data: dict):
    print("Мы попали в хэндлер")
    await call.message.edit_text("Вы обратились в техподдержку. Ждем ответа от оператора!")
    user_id = int(callback_data.get("user_id"))

    print(f"Это id менеджера {user_id=}")

    if not await keyboards.check_support_available(user_id):
        support_id = await keyboards.get_support_manager()
    else:
        support_id = user_id

    if not support_id:
        await call.message.edit_text("К сожалению, сейчас нет свободных операторов. Попробуйте позже.")
        await state.reset_state()
        return

    await state.set_state("wait_in_support")

    print(f"Это кому присваивается state {state.user}")
    print(f"А это его state {await state.get_state()}")

    await state.update_data(second_id=support_id)
    user_id = call.from_user.id

    keyboard = await keyboards.kb_support(messages="many", user_id=call.from_user.id)
    await call.bot.send_message(support_id,
                           f"С вами хочет связаться пользователь {call.from_user.full_name}",
                           reply_markup=keyboard
                           )


async def answer_support_call(call: types.CallbackQuery,
                              state: FSMContext,
                              callback_data: dict):
    second_id = callback_data.get("user_id")

    print(f"{second_id=}")

    dp = Dispatcher.get_current()
    user_state = dp.current_state(chat=second_id, user=second_id)

    if str(await user_state.get_state()) != "wait_in_support":
        await call.message.edit_text("К сожалению, пользователь уже передумал.")
        return

    await state.set_state("in_support")
    await user_state.set_state("in_support")

    await state.update_data(second_id=second_id)

    keyboard = keyboards.cancel_support(second_id)
    keyboard_second_user = keyboards.cancel_support(call.from_user.id)

    await call.message.edit_text("Вы на связи с пользователем!\n"
                                 "Чтобы завершить общение нажмите на кнопку.",
                                 reply_markup=keyboard
                                 )
    await call.bot.send_message(second_id,
                           "Техподдержка на связи! Можете писать сюда свое сообщение. \n"
                           "Чтобы завершить общение нажмите на кнопку.",
                           reply_markup=keyboard_second_user
                           )


async def not_supported(message: types.Message, state: FSMContext):
    data = await state.get_data()
    second_id = data.get("second_id")

    keyboard = keyboards.cancel_support(second_id)
    await message.answer("Дождитесь ответа оператора или отмените сеанс", reply_markup=keyboard)


async def exit_support(call: types.CallbackQuery, state: FSMContext, callback_data: dict, storage=MemoryStorage()):
    user_id = int(callback_data.get("user_id"))
    dp = Dispatcher.get_current()
    second_state = dp.current_state(chat=user_id, user=user_id)

    if await second_state.get_state() is not None:
        data_second = await second_state.get_data()
        second_id = data_second.get("second_id")
        if int(second_id) == call.from_user.id:
            await second_state.reset_state()
            await call.bot.send_message(user_id, "Пользователь завершил сеанс техподдержки")

    await call.message.edit_text("Вы завершили сеанс")
    await state.reset_state()


async def share_phone_number(call: types.CallbackQuery):
    text = "А еще можете поделиться Вашим телефонным номером"
    keyboard = await keyboards.kb_share_phone()
    await call.message.edit_text(text=text)
    await call.message.answer(text="Нажми кнопку ниже", reply_markup=keyboard)
    await call.answer()


async def get_phone(message: types.Message):
    contact = message.contact
    db.update_user_phone(contact.phone_number, contact.user_id)

    await message.copy_to(support_ids[0])
    await message.answer(
        f"Спасибо, {contact.full_name}\n"
        f"Ваш номер {contact.phone_number} был получен и передан менеджеру. "
        f"Ожидайте",
        reply_markup=types.ReplyKeyboardRemove()
    )


def register_handlers_call_Support(dp: Dispatcher):
    dp.register_callback_query_handler(ask_suport_call,
                                       help_callback.filter(), state="*")
    dp.register_callback_query_handler(
            send_to_support_call,
            support_callback.filter(messages="many", as_user="yes"), state="*")
    dp.register_message_handler(not_supported,
                                state="wait_in_support",
                                content_types=types.ContentTypes.ANY)
    dp.register_callback_query_handler(
                            exit_support,
                            cancel_support_callback.filter(),
                            state=["in_support", "wait_in_support", None])
    dp.register_callback_query_handler(answer_support_call,
                                       support_callback.filter(messages="many",
                                                               as_user="no"), state="*")

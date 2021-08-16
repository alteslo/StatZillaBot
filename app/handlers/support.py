from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext

from app.config_reader import load_config
from app.states.interview import Interview
from app import keyboards
from app.keyboards.callback_datas import support_callback


config = load_config("config/bot.ini")
bot = Bot(token=config.tg_bot.token)


async def ask_suport(message: types.Message):
    text = "Хотите написать сообщение техподдержке? Нажмите на кнопку ниже!"
    keyboard = await keyboards.kb_support(messages="one")
    await message.answer(text=text, reply_markup=keyboard)
    print(f"Выводим id из ask_support {message.from_user.id}")


async def send_to_support(call: types.CallbackQuery,
                          state: FSMContext,
                          callback_data: dict):
    print(callback_data)
    user_id = int(callback_data.get("user_id"))
    await call.answer()

    await call.message.answer(
        "Пришлите ваше сообщение, которым вы хотите поделиться")
    await Interview.wait_for_support_message.set()
    await state.update_data(second_id=user_id)
    data = await state.get_state()

    print(data)
    print(f"user_id={user_id}")


async def get_support_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    second_id = data.get("second_id")

    print(f"second_id={second_id}")

    await bot.send_message(second_id,
                        "Вам письмо! Вы можете ответить нажав на кнопку ниже")

    print(f"user.id из get_support_message = {message.from_user.id}")

    keyboard = await keyboards.kb_support(messages="one",
                                          user_id=message.from_user.id)
    await message.copy_to(second_id, reply_markup=keyboard)

    await message.answer("Вы отправили это сообщение!")
    await state.reset_state()


def register_handlers_Support(dp: Dispatcher):
    dp.register_message_handler(ask_suport, commands="support", state="*"),
    dp.register_callback_query_handler(
            send_to_support,
            support_callback.filter(messages="one"), state="*")
    dp.register_message_handler(get_support_message,
                                content_types=types.ContentTypes.ANY,
                                state=Interview.wait_for_support_message)

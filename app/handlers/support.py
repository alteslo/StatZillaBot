from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from app import keyboards
from app.config_reader import load_config
from app.states.interview import Interview
from app.keyboards.callback_datas import support_callback
from app.keyboards.callback_datas import help_callback
from app.utils.db_api.sqlite import db
from app.data.app_data import support_ids


config = load_config("config/bot.ini")
bot = Bot(token=config.tg_bot.token)


async def ask_suport(call: types.CallbackQuery):
    text = "Напишите нашему менеджеру - <b>нажав на кнопку!</b>"
    keyboard = await keyboards.kb_support(messages="one")
    await call.message.edit_text(text=text,
                                 parse_mode='HTML',
                                 reply_markup=keyboard)
    await call.answer()


async def send_to_support(call: types.CallbackQuery,
                          state: FSMContext,
                          callback_data: dict):
    print(callback_data)
    user_id = int(callback_data.get("user_id"))
    text = "Пришлите Ваше сообщение, которым вы хотите поделиться"

    await call.message.answer(text=text)
    await Interview.wait_for_support_message.set()
    await state.update_data(second_id=user_id)
    await call.answer()

    data = await state.get_state()
    print(data)
    print(f"user_id={user_id}")


async def get_support_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    second_id = data.get("second_id")

    print(f"second_id={second_id}")

    await bot.send_message(
        second_id,
        "Вам письмо! Вы можете ответить нажав на кнопку ниже")

    keyboard = await keyboards.kb_support(messages="one",
                                          user_id=message.from_user.id)
    await message.copy_to(second_id, reply_markup=keyboard)

    await message.answer("Вы отправили это сообщение!")
    await state.reset_state()


async def share_phone_number(call: types.CallbackQuery):
    text = "А еще можете поделиться Вашим телефонным номером"
    keyboard = await keyboards.kb_share_phone()

    # Изменяем исходное сообщение, убиваем клавиатуру и высылаем новое
    # сообщение с кнопкой поделиться телефоном
    await call.message.edit_text(text=text)
    await call.message.answer(text="Нажми кнопку ниже", reply_markup=keyboard)
    await call.answer()


async def get_phone(message: types.Message):
    contact = message.contact
    db.update_user_phone(contact.phone_number, contact.user_id)

    await message.copy_to(support_ids[0])
    await message.answer(
                         text=f"Спасибо, {contact.full_name}\n"
                              f"Ваш номер {contact.phone_number} был получен "
                              f"и передан менеджеру.\n"
                              f"Ожидайте",
                         reply_markup=types.ReplyKeyboardRemove())


def register_handlers_Support(dp: Dispatcher):
    dp.register_callback_query_handler(ask_suport,
                                       help_callback.filter(), state="*")
    dp.register_callback_query_handler(share_phone_number,
                                       Text(equals="share_phone"),
                                       state="*")
    dp.register_message_handler(get_phone,
                                content_types=types.ContentType.CONTACT,
                                state="*")
    dp.register_callback_query_handler(send_to_support,
                                       support_callback.filter(messages="one"),
                                       state="*")
    dp.register_message_handler(get_support_message,
                                content_types=types.ContentTypes.ANY,
                                state=Interview.wait_for_support_message)

from aiogram import types, Dispatcher
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware


class SupportMiddleware(BaseMiddleware):

    async def on_pre_process_message(self, message: types.Message, data: dict):
        # Для начала достанем состояние текущего пользователя,
        # так как state: FSMContext нам сюда не прилетит
        dp = Dispatcher.get_current()
        state = dp.current_state(chat=message.from_user.id, user=message.from_user.id)

        # Получим строчное значение стейта и сравним его
        state_str = str(await state.get_state())
        if state_str == "in_support":

            # Заберем айди второго пользователя и отправим ему сообщение
            data = await state.get_data()
            second_id = data.get("second_id")
            await message.copy_to(second_id)

            # Не пропустим дальше обработку в хендлеры
            raise CancelHandler()


def register_middlewares(dp: Dispatcher):
    dp.setup_middleware(SupportMiddleware())

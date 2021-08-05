from aiogram.utils.callback_data import CallbackData

service_callback = CallbackData("service", "bot_settings")
share_callback = CallbackData("share", "id")
buy_callback = CallbackData("buy", "id")
like_callback = CallbackData("action", "action", "id")

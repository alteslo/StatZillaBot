
from aiogram.dispatcher.filters.state import State, StatesGroup


class Interview(StatesGroup):
    waiting_for_service_selection = State()
    waiting_for_stat_processing_choice = State()
    price_answer = State()
    waiting_for_contact_number = State()

    wait_for_support_message = State()

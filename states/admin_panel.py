from aiogram.dispatcher.filters.state import StatesGroup, State


class StatesAP(StatesGroup):
    start = State()
    set_text = State()
    get_file = State()
    delete_file = State()

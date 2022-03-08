from aiogram.dispatcher.filters.state import State, StatesGroup

class FlatState(StatesGroup):
    address = State()
    add_info = State()

class DelFlatState(StatesGroup):
    flat_id = State()
    confirm = State()

class SearchFlatState(StatesGroup):
    flat_id = State()
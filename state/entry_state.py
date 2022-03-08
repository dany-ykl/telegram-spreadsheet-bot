from aiogram.dispatcher.filters.state import StatesGroup, State


class EntryState(StatesGroup):
    tablename = State()
    date_entry = State()
    date_exit = State()
    name_renter = State()
    phone = State()
    amount = State()
    
class DelEntryState(StatesGroup):
    tablename = State()
    entry_id = State()
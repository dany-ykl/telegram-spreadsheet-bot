import email
from aiogram.dispatcher.filters.state import State, StatesGroup

class EditState(StatesGroup):
    email = State()

class EditUpdateState(StatesGroup):
    email = State()

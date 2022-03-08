from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from service import auth
from keybords.client_keybord import get_start_command_kb


cancel = ['🛑 Отмена', 'нет', 'Нет', '/cancel']

@dp.message_handler(commands=['start', 'menu'])
@auth
async def start_command(message:types.Message):
    poll_keybord = get_start_command_kb()
    await message.answer('Выберите нужную операцию:', reply_markup=poll_keybord)


@dp.message_handler(lambda message: message.text in cancel, state='*')
async def cancel_command(message:types.Message, state:FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer('Мы ещё ничего не сделали!', reply_markup=get_start_command_kb())
        return

    await state.reset_state()
    await message.answer('Действие отменено', reply_markup=get_start_command_kb())
   

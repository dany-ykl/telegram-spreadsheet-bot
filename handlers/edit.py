from aiogram import types
from aiogram.dispatcher import FSMContext

from state.edit_state import EditState, EditUpdateState
from keybords.client_keybord import edit_kb, get_start_command_kb
from loader import dp
from db.database import DB

db = DB()

@dp.message_handler(lambda message: message.text=='⚙ Настройки')
async def get_edit_keyboard(message:types.Message):
    await message.answer('Выберете нужную операцию:', reply_markup=edit_kb())

@dp.message_handler(lambda message: message.text=='Мой email')
async def get_data_user(message:types.Message):
    try:
        user = db.get_user(user_id=message['from']['id'])
        await message.answer(f'{user["email"]}')
    except:
        await message.answer('Вы не сохроняли email!')

@dp.message_handler(lambda message: message.text=='Удалить email')
async def delete_email(message:types.Message):
    try:
        db.delete_user(user_id=message['from']['id'])
        await message.answer('Email успешно удален!')
    except:
        await message.answer('Вы не сохроняли email!')

@dp.message_handler(lambda message: message.text=='Обновить email', state=None)
async def enter_to_update_state(message:types.Message):
    await message.answer('Введите новый email:')
    await EditUpdateState.email.set()

@dp.message_handler(state=EditUpdateState.email)
async def update_email(message:types.Message, state:FSMContext):
    await state.update_data(email=message.text)
    edit_data = await state.get_data()
    await state.finish()
    try:
        db.update_user_email(user_id=message['from']['id'], email=edit_data['email'])
        await message.answer(f'Email: {edit_data["email"]} успешно сохранён!', reply_markup=get_start_command_kb())
    except:
        await message.answer('Вы не сохроняли email!')


@dp.message_handler(lambda message: message.text=='Указать email', state=None)
async def enter_to_edit_state(message:types.Message):
    await message.answer('Введите email:')
    await EditState.email.set()

@dp.message_handler(state=EditState.email)
async def email_step(message:types.Message, state:FSMContext):
    email = message.text.lower()
    await state.update_data(email=email)
    await state.update_data(user_id=str(message['from']['id']))
    edit_data = await state.get_data()
    await state.finish()
    try:
        db.add_user(user_id=edit_data['user_id'], email=edit_data['email'])
        await message.answer(f'Email: {email} успешно сохранён!', reply_markup=get_start_command_kb())
    except:
        await message.answer('Email адрес уже существует! Удалите его или измените')






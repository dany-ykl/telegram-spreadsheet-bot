from random import randint

from aiogram import types
from aiogram.dispatcher import FSMContext


from loader import dp
from state.flat_state import FlatState
from google_sheets import spreadsheet
from db.database import DB


db = DB()
template_link = 'https://docs.google.com/spreadsheets/d/'

@dp.message_handler(lambda message: message.text=='🏠 Добавить квартиру', state=None)
async def enter_to_flat_state(message:types.Message):
    await message.answer('Введите адрес:')
    await FlatState.address.set()

@dp.message_handler(state=FlatState.address)
async def address_step(message:types.Message, state:FSMContext):
    address_answer = message.text.lower()
    email = db.get_user(message['from']['id'])['email']
    await state.update_data(address=address_answer)
    await state.update_data(email=email)
    await message.answer('Введите дополнительную информацию:\n'
    '<i>(необязательно)</i>', parse_mode='HTML')
    await FlatState.add_info.set()

@dp.message_handler(state=FlatState.add_info)
async def additional_info_step(message:types.Message, state:FSMContext):
    add_info_answer = message.text
    await state.update_data(add_info=add_info_answer)
    await state.update_data(flat_id=str(randint(100, 900)))
    flat_data = await state.get_data()
    await state.finish() 
    await message.answer('Пожалуйста подождите...')
    try:
        gs = spreadsheet.GoogleSheet(email=flat_data['email'])
        sheets = gs.create_worksheet(tablename=flat_data['address'],
                                     add_info=flat_data['add_info'])
        await message.answer("Данные успешно сохранены!\n\n"
        f"id таблицы: <i>{flat_data['flat_id']}</i>\n"
        f"Адрес квартиры: <i>{flat_data['address']}</i>\n"
        f"Дополнительная информация: <i>{flat_data['add_info']}</i>\n\n"
        f"таблица: {template_link+str(sheets['sheet'].id)}"
        , parse_mode='HTML')
    except:
        await message.answer('Email не существует или не привязан к GoogleSheet!')
    
    

    
    
    


from aiogram import types
from aiogram.dispatcher.filters import Text

from loader import dp
from keybords.client_keybord import get_start_command_kb, information, \
                                    flat_information, entry_information
from db.database import DB
from google_sheets import spreadsheet

db = DB()

@dp.message_handler(lambda message: message.text=='📖 Информация')
async def get_information(message:types.Message):
    await message.answer('Что хотите узнать?',reply_markup=information())

@dp.message_handler(lambda message: message.text=='Квартиры')
async def get_flat_information(message:types.Message):
    await message.answer('Выберите нужное:', reply_markup=flat_information())

@dp.message_handler(lambda message: message.text=='Записи')
async def get_flat_information(message:types.Message):
    await message.answer('Выберите нужное:', reply_markup=entry_information())

@dp.message_handler(lambda message: message.text=='Все квартиры')
async def get_flat_information(message:types.Message):
    try:
        email = db.get_user(user_id=message['from']['id'])['email']
        gs = spreadsheet.GoogleSheet(email)
        worksheet_list = gs.get_all_worksheet()
        for worksheet in worksheet_list:
            await message.answer(f'Адрес: {worksheet.title}')
        await message.answer(f'Список квартир получен', reply_markup=get_start_command_kb())
    except AttributeError:
        await message.answer('Проверте сохроняли ли вы email и\
            есть ли у вас внесенные квартиры', reply_markup=get_start_command_kb())

@dp.message_handler(lambda message: message.text=='Записи по квартире')
async def get_entry_of_flat(message:types.Message):
    keyboard = types.InlineKeyboardMarkup()
    try:
        email = db.get_user(user_id=message['from']['id'])['email']
        gs = spreadsheet.GoogleSheet(email)
        worksheet_list = gs.get_all_worksheet()
        for worksheet in worksheet_list:
            keyboard.add(types.InlineKeyboardButton(text=worksheet.title,
                                                    callback_data=f"get entry: {worksheet.title}"))

        await message.answer("Выберите квартиру:", reply_markup=keyboard)
    except AttributeError:
        await message.answer('Проверте сохроняли ли вы email и\
            есть ли у вас внесенные квартиры', reply_markup=get_start_command_kb())

@dp.callback_query_handler(Text(startswith='get entry: '))
async def sdelete_worksheet(call: types.CallbackQuery):
    tablename = str(call.data).replace('get entry: ', '')
    email = db.get_user(user_id=call['from']['id'])['email']
    try:
        gs = spreadsheet.GoogleSheet(email)
        entries = gs.get_entries(tablename)
        await call.message.answer(entries) 
        await call.answer()
    except:
        await call.message.answer('Возможно в таблице отсутствуют записи...')
        await call.answer()




    
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from loader import dp
from state.entry_state import DelEntryState
from keybords.client_keybord import get_start_command_kb
from google_sheets import spreadsheet
from db.database import DB
from google_sheets.validation import EntryId

db = DB()

@dp.message_handler(lambda message: message.text=='❌ Удалить запись', state=None)
async def enter_to_del_entry_state(message:types.Message):
    await message.answer('Загружаем список квартир...')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    try:
        email = db.get_user(user_id=message['from']['id'])['email']
        gs = spreadsheet.GoogleSheet(email)
        worksheet_list = gs.get_all_worksheet()
        for worksheet in worksheet_list:
            keyboard.add(types.KeyboardButton(text=f'Квартира: {worksheet.title}'))
        await message.answer('Выберите квартиру:', reply_markup=keyboard)
        await DelEntryState.tablename.set()
    except:
        await message.answer('Проверте сохроняли ли вы email и\
            есть ли у вас внесенные квартиры', reply_markup=get_start_command_kb())

@dp.message_handler(Text(startswith='Квартира: '), state=DelEntryState.tablename)
async def tablename_step(message:types.Message, state:FSMContext):
    tablename = str(message.text).replace('Квартира: ', '')
    email = db.get_user(user_id=message['from']['id'])['email']
    await state.update_data(email=email)
    await state.update_data(tablename=tablename)
    await DelEntryState.entry_id.set()
    await message.answer('Введите id записи:\n'
        'если не знаете можно посмотреть в разделе "Информация" или GoogleSheets',
        reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(state=DelEntryState.entry_id)
async def flat_id_step(message:types.Message, state:FSMContext):
    entry_id = message.text
    if entry_id.isdigit() and len(entry_id) == 3:
        await state.update_data(entry_id=message.text)
        entry_data = await state.get_data()
        await state.finish()
        entry = EntryId.parse_obj(entry_data)
        try:
            gs = spreadsheet.GoogleSheet(entry.email)
            gs.delete_entry(entry)
            await message.answer(f'Запись {entry.entry_id} успешно удалена!', reply_markup=get_start_command_kb())
        except:
            message.answer('Ячейка не сушествует!', reply_markup=get_start_command_kb())
    else:
        await message.answer('Некорректный формат записи! Попробуйте еще раз\n'
        '<i>id должен состоять из 3 цифр!</i>', parse_mode='HTML')

        
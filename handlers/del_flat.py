from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from loader import dp
from state.flat_state import DelFlatState
from keybords.client_keybord import check_action, get_start_command_kb
from db.database import DB
from google_sheets import spreadsheet

db = DB()

        
@dp.message_handler(lambda message: message.text=='❌ Удалить квартиру')
async def get_worksheet_inline(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    try:
        email = db.get_user(user_id=message['from']['id'])['email']
        gs = spreadsheet.GoogleSheet(email)
        worksheet_list = gs.get_all_worksheet()
        for worksheet in worksheet_list:
            keyboard.add(types.InlineKeyboardButton(text=worksheet.title,
                                                    callback_data=f"del address: {worksheet.title}"))

        await message.answer("Выберите квартиру:", reply_markup=keyboard)
    except AttributeError:
        await message.answer('Проверте сохроняли ли вы email и\
            есть ли у вас внесенные квартиры', reply_markup=get_start_command_kb())

    

@dp.callback_query_handler(Text(startswith='del address: '))
async def sdelete_worksheet(call: types.CallbackQuery):
    tablename = str(call.data).replace('del address: ', '')
    email = db.get_user(user_id=call['from']['id'])['email']
    try:
        gs = spreadsheet.GoogleSheet(email)
        gs.delete_worksheet(tablename)
        await call.message.answer(f"{tablename} успешно удалена") 
        await call.answer()
    except:
        await call.message.answer('Извините, это единственный лист в таблице!\n'
                                  'Удалить можно только всю таблицу в приложении GoogleSheets (\n'
                                  'Если вам нужно удалить имеенно этот лист, то вы можите\n'
                                  'создать новую квартиру и затем удалить ненужный лист таблицы.')
        await call.answer()
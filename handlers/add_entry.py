from random import randint

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from keybords.client_keybord import get_start_command_kb
from state.entry_state import EntryState
from loader import dp
from service import validate_date
from google_sheets.validation import Entry
from google_sheets import spreadsheet
from db.database import DB


db = DB()

@dp.message_handler(lambda message: message.text=='✍ Добавить запись', state=None)
async def enter_to_entry_state(message:types.Message):
    await message.answer('Загружаем список квартир...')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    try:
        email = db.get_user(user_id=message['from']['id'])['email']
        gs = spreadsheet.GoogleSheet(email)
        worksheet_list = gs.get_all_worksheet()
        for worksheet in worksheet_list:
            keyboard.add(types.KeyboardButton(text=f'Адрес: {worksheet.title}'))
        await message.answer('Выберите квартиру:', reply_markup=keyboard)
        await EntryState.tablename.set()
    except:
        await message.answer('Проверте сохроняли ли вы email и\
            есть ли у вас внесенные квартиры', reply_markup=get_start_command_kb())

@dp.message_handler(Text(startswith='Адрес: '), state=EntryState.tablename)
async def tablename_step(message:types.Message, state:FSMContext):
    tablename = str(message.text).replace('Адрес: ', '')
    email = db.get_user(user_id=message['from']['id'])['email']
    await state.update_data(email=email)
    await state.update_data(tablename=tablename)
    await EntryState.date_entry.set()
    await message.answer('Введите дату възда:\n'
        '<i>Пример: 20-11-2022</i>', parse_mode='HTML', reply_markup=types.ReplyKeyboardRemove())
    
@dp.message_handler(state=EntryState.date_entry)
async def date_entry_step(message:types.Message, state:FSMContext):
    date_entry = str(message.text).strip()
    if validate_date(str(date_entry)):
        await state.update_data(date_entry=date_entry)
        await EntryState.date_exit.set()
        await message.answer('Введите дату выезда:\n'
        '<i>Пример: 20-11-2022</i>', parse_mode='HTML')
    else:
        await message.answer('Некорректный формат даты! Попробуйте еще раз')

@dp.message_handler(state=EntryState.date_exit)
async def date_exit_step(message:types.Message, state:FSMContext):
    date_exit = str(message.text).strip()
    if validate_date(str(date_exit)):
        await state.update_data(date_exit=date_exit)
        await message.answer('Введите имя арендатора:\n'
        '<i>Также можете ввести фамилию</i>', parse_mode='HTML')
        await EntryState.name_renter.set()
    else:
        await message.answer('Некорректный формат даты! Попробуйте еще раз')
    
@dp.message_handler(state=EntryState.name_renter)
async def name_renter_step(message:types.Message, state:FSMContext):
    name = str(message.text).strip()
    if name.replace(' ', '').isalpha():
        await state.update_data(name_renter=name)
        await message.answer('Введите номер телефона:\n')
        await EntryState.phone.set()
    else:
        await message.answer('Некорректный формат имени! Попробуйте еще раз')

@dp.message_handler(state=EntryState.phone)
async def phone_step(message:types.Message, state:FSMContext):
    phone = str(message.text).strip()
    if phone.isdigit():
        await state.update_data(phone=phone)
        await message.answer('Введите сумму оплаты:')
        await EntryState.amount.set()
    else:
        await message.answer('Некорректный формат номера! Попробуйте еще раз')

@dp.message_handler(state=EntryState.amount)
async def amount_step(message:types.Message, state:FSMContext):
    amount = message.text.strip().replace('₽','')
    if amount.isdigit():
        await state.update_data(amount=amount)
        await state.update_data(entry_id=str(randint(100, 900)))
        entry_data = await state.get_data()
        await state.finish()
        entry = Entry.parse_obj(entry_data)
        try:
            gs = spreadsheet.GoogleSheet(entry.email)
            gs.create_entry(entry)
            await message.answer("Данные успешно сохранены!\n\n"
            f"id записи: <i>{entry.entry_id}</i>\n"
            f"Дата въезда: <i>{entry.date_entry}</i>\n"
            f"Дата выезда: <i>{entry.date_exit}</i>\n"
            f"Имя арендатора: <i>{entry.name_renter}</i>\n"
            f"Телефон: <i>{entry.phone}</i>\n"
            f"Сумма: <i>{entry.amount}₽</i>\n", parse_mode='HTML', reply_markup=get_start_command_kb())
        except:
            message.answer('Произошка ошибка. Попробуйте ещё раз!', reply_markup=get_start_command_kb())
            
    else:
        await message.answer('Некорректный формат суммы! Попробуйте еще раз')
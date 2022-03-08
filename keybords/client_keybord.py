from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_start_command_kb():
    poll_keybord = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    add_flat = KeyboardButton(text='🏠 Добавить квартиру')
    add_entry = KeyboardButton(text='✍ Добавить запись')
    del_flat = KeyboardButton(text='❌ Удалить квартиру')
    del_entry = KeyboardButton(text='❌ Удалить запись')
    info = KeyboardButton(text='📖 Информация')
    cancel = KeyboardButton(text='🛑 Отмена')
    edit = KeyboardButton(text='⚙ Настройки')
    
    poll_keybord.row(add_flat, add_entry).row(del_flat, del_entry).row(info, cancel).add(edit)

    return poll_keybord

def check_action():
    poll_keybord = ReplyKeyboardMarkup(resize_keyboard=True)

    yes = KeyboardButton(text='Да')
    no = KeyboardButton(text='Нет')

    poll_keybord.row(yes, no)

    return poll_keybord

def information():
    poll_keybord = ReplyKeyboardMarkup(resize_keyboard=True)

    flat_info = KeyboardButton(text='Квартиры')
    entry_info = KeyboardButton(text='Записи')
    cancel = KeyboardButton(text='🛑 Отмена')

    poll_keybord.row(flat_info, entry_info).add(cancel)

    return poll_keybord

def entry_information():
    poll_keybord = ReplyKeyboardMarkup(resize_keyboard=True)

    flat_entry_info = KeyboardButton(text='Записи по квартире')
    cancel = KeyboardButton(text='🛑 Отмена')

    poll_keybord.row(flat_entry_info, cancel)

    return poll_keybord

def flat_information():
    poll_keybord = ReplyKeyboardMarkup(resize_keyboard=True)

    all_flat_info = KeyboardButton(text='Все квартиры')
    cancel = KeyboardButton(text='🛑 Отмена')

    poll_keybord.add(all_flat_info, cancel)

    return poll_keybord

def edit_kb():
    poll_keybord = ReplyKeyboardMarkup(resize_keyboard=True)

    email = KeyboardButton(text='Указать email')
    my_email = KeyboardButton(text='Мой email')
    update_email = KeyboardButton(text='Обновить email')
    del_email = KeyboardButton(text='Удалить email')


    poll_keybord.row(email, my_email).row(update_email, del_email)

    return poll_keybord 


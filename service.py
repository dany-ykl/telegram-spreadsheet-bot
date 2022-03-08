import re
import datetime

import config

def auth(func):
    async def wrapper(message):
        if str(message['from']['id']) not in config.ID:
            await message.answer(message['from']['id'])
            return await message.reply('Access denied', reply=False)    
        return await func(message)
    return wrapper

def validate_date(date):
    try:
        datetime.datetime.strptime(date, "%d-%m-%Y")
        return True
    except:
        return False

def validate_amount(amount):
    if re.search(r'[^a-zA-Zа-яА-Я]', amount):
        return False
    else:
        return True
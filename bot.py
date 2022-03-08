from aiogram import types

from loader import bot


async def set_default_command(dp):
    await bot.set_my_commands([
        types.BotCommand(command='start', description='Запустить бота'),
        types.BotCommand(command='menu', description='Меню'),
        types.BotCommand(command='cancel', description='Отмена')
    ])

if __name__=='__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, skip_updates=True, on_startup=set_default_command)
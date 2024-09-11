import asyncio
from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from handlers import handlers
from routers import admins, channels, mess, navigation, search


bot = Bot(token="6904548902:AAG44Ny4Yvf15O9VOhHEnMYTKleSg1W0pUM",
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def main():
    dp = Dispatcher()

    dp.include_routers(
        handlers.router,
        admins.router,
        channels.router,
        navigation.router,
        search.router,
        mess.router,
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=[])

if __name__ == "__main__":
    asyncio.run(main())

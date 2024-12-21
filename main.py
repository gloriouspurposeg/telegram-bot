import os
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.bot import DefaultBotProperties
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage
from database.models import async_main
import asyncio
from handlers.user_handlers import router as user_router
from handlers.admin_handlers import router as admin_router
from middlewares.access_middleware import AccessMiddleware
from dotenv import load_dotenv

async def main():
    await async_main()
    # Botni ishga tushirish
    load_dotenv()
    bot = Bot(
        token=os.getenv('BOT_TOKEN'),
        session=AiohttpSession(),
        default=DefaultBotProperties(parse_mode="HTML")
    )
    dp = Dispatcher(storage=MemoryStorage())
    
    # Routerlarni ro'yxatdan o'tkazish
    dp.include_router(user_router)
    dp.include_router(admin_router)

    # Middlewarelarni ro'yxatdan o'tkazish
    # dp.message.middleware.register(lambda m, d: d.update(bot=bot))
    # dp.message.middleware.register(AccessMiddleware())
    
    print("Bot ishga tushdi!")
    try:
        # Botni polling rejimida ishga tushirish
        await dp.start_polling(bot)

    finally:
        # Resurslarni tozalash
        await bot.session.close()

if __name__ == "__main__":
    try: 
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot to'xtatildi!")

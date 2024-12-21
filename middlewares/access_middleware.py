from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable
from database.requests import is_admin

class AccessMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any]
    ) -> Any:
        # Foydalanuvchining ID'sini olish
        user_id = event.from_user.id

        # Admin ekanligini tekshirish
        if event.text and (event.text.startswith("TOP 25 Referallar") or event.text.startswith("Xabar yuborish")):
            pool = data.get("pool")  # Middleware orqali `pool` ni olish
            if not pool:
                raise ValueError("Database pool mavjud emas!")

            if not await is_admin(user_id):  # `pool` ni `is_admin` ga yuborish
                await event.reply("Bu buyruq faqat adminlar uchun!")  # To'g'ri metodni ishlatish
                return

        # Handlerni chaqirish
        return await handler(event, data)

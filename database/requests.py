from aiogram import Bot
from database.models import async_session
from database.models import User, Channel, Admin
from sqlalchemy import select, func, desc, update

#user kiritish
async def set_user(chat_id: int, refer: int, name: str) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.chat_id == chat_id))

        if not user:
            referr_id = None
            if refer and await get_user(refer):
                referr_id = refer

            session.add(User(chat_id=chat_id,
                             first_name= name,
                             referals_count = 0,
                             refer_id = referr_id
                             ))
            await session.commit()

# Adminni tekshirish
async def is_admin(user_id):
    async with async_session() as session:
        return await session.scalar(select(Admin.chat_id).where(Admin.chat_id == user_id))

# Foydalanuvchining referallar sonini olish
async def get_user(user_id):
    async with async_session() as session:
        return await session.scalar(select(User).where(User.id == user_id))

# Foydalanuvchining referallar sonini olish
async def get_user_referrals_count(user_id):
    async with async_session() as session:
        return await session.scalar(select(func.count()).select_from(User).where(User.refer_id == user_id))

# Botdan foydalanuvchilar sonini olish
async def get_total_users():
    async with async_session() as session:
        return await session.scalar(select(func.count()).select_from(User))

# Barcha kanallarni olish
async def get_channels():
    async with async_session() as session:
        return await session.scalars(select(Channel))

# referallar sonini oshishi
async def add_referal(refer: int):
    async with async_session() as session:
        await session.scalar(select(User).where(User.chat_id == refer).update({'referals_count': select(User.referals_count).where(User.chat_id == refer)+1 }))
        await session.commit()

# TOP 25 referallarni olish
async def get_top_referrers(limit = 25):
    async with async_session() as session:
        if await get_total_users() > limit: 
            result = await session.scalars(
                select(User)
                .order_by(desc(User.referals_count))
                .limit(limit)
            )
            return result.all() 
        else:
            result = await session.scalars(
                select(User)
                .order_by(desc(User.referals_count))
            )
            return result.all() 

# Hamma foydalanuvchilarga xabar yuborish
async def get_all_users():
    async with async_session() as session:
        return await session.scalars(select(User))

# Kanalga obuna bo'lganligini tekshirish
async def is_user_subscribed(bot: Bot, user_id: int, channel_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception:
        return False
async def check_all_channels(bot: Bot, user_id: int) -> bool:
    channels = await get_channels()  # Barcha kanallarni databasedan olish
    if channels:
        for channel in channels:
            channel_id = channel.chat_id
            if not await is_user_subscribed(bot, user_id, channel_id):
                return False  # Foydalanuvchi barcha kanallarga obuna bo'lmasa, False qaytaradi
        return True
    else:
        return True




from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from database import requests as rqs

router = Router()

# Admin uchun inline keyboard
admin_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Umumiy foydalanuvchilar soni", callback_data="total_users")],
        [InlineKeyboardButton(text="Xabar yuborish", callback_data="send_message")],
    ]
)

async def send_message_to_all(message):
    try:
        users = await rqs.get_all_users()
        for user in users:
            if message.from_user.id != user.chat_id:
                await message.bot.send_message(
                    chat_id=user.chat_id,
                    text=message.text
                )
        return True
    except Exception:
        return False

@router.message(Command("admin"))
async def admin_panel(message: Message):
    if await rqs.is_admin(message.from_user.id):
        await message.answer("Admin paneliga xush kelibsiz!", reply_markup=admin_inline_keyboard)

@router.callback_query(F.data == "total_users")
async def show_total_users(callback_query: types.CallbackQuery):
    if await rqs.is_admin(callback_query.from_user.id):
        total_users = await rqs.get_total_users()
        await callback_query.message.edit_text(f"Botdan {total_users} foydalanuvchi foydalanmoqda.")

@router.callback_query(F.data == "send_message")
async def send_message_to_users(callback_query: types.CallbackQuery):
    if await rqs.is_admin(callback_query.from_user.id):
        await callback_query.message.edit_text("Hamma foydalanuvchilarga yuboriladigan xabarni kiriting:")

@router.message(lambda message: message.reply_to_message and message.reply_to_message.text == "Hamma foydalanuvchilarga yuboriladigan xabarni kiriting:")
async def handle_broadcast_message(message: Message):
    if await rqs.is_admin(message.from_user.id):
        if await send_message_to_all(message):
            await message.answer("Xabar muvaffaqiyatli yuborildi.")
        else:
            await message.answer("Xabar yuborishda xatolik.")

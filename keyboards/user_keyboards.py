from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Foydalanuvchilar uchun keyboard
user_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Referallar soni"), KeyboardButton(text="Statistika")],
    ],
    resize_keyboard=True,
)

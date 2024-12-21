from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Admin uchun keyboard
admin_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="TOP 25 Referallar"), KeyboardButton(text="Umumiy foydalanuvchilar soni")],
        [KeyboardButton(text="Xabar yuborish")],
    ],
    resize_keyboard=True,
)

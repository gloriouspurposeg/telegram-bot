from aiogram import Router, types, F, Bot
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message,InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from database import requests as rqs
from aiogram.filters.callback_data import CallbackData

class ConfirmSubscriptionCallback(CallbackData, prefix="confirm_subscription"):
    pass

router = Router()

# Foydalanuvchi uchun keyboard
user_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Referallar soni"), KeyboardButton(text="TOP 50 Referlar")],
        [KeyboardButton(text="Referal havolasini olish")],
    ],
    resize_keyboard=True,
)
# Kanallarga obuna bo'lganligini tekshirish
async def message_for_channel(message: Message):
    if not await rqs.check_all_channels(message.bot, message.from_user.id):
        channels = await rqs.get_channels()
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"👉 {channel.name}", url=channel.link)] for channel in channels
        ] + [
            [InlineKeyboardButton(text="Tasdiqlansin", callback_data="confirm_subscription")]
        ])
        await message.answer(
            "Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling:\n\n", reply_markup=keyboard
        )
        return False
    else :
        return True
    
@router.callback_query(ConfirmSubscriptionCallback.filter())
async def confirm_subscription_callback(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    bot = callback_query.bot

    if await rqs.check_all_channels(bot, user_id):
        await callback_query.message.edit_text(
            "Quyidagi buyriqlardan birini tanlang:"
        )
    else:
        await callback_query.answer(
            "Iltimos, kanallarga obuna bo'lganingizni tekshiring va qayta urinib ko'ring.", show_alert=True
        )
#START
@router.message(CommandStart()) #https://t.me/kariymulloh_referalbot?start=r_id
async def start_handler(message: Message, command: CommandObject):
    chat_id = message.from_user.id
    first_name = message.from_user.first_name
    referral_id = None
    if command.args:
        option, value = command.args.split("_")
        match option:
            case "r":
                try:
                    referral_id = int(value)
                except ValueError:
                    return None

    await rqs.set_user(message.from_user.id, referral_id, first_name)

    if not await message_for_channel(message):
        return

    # Agar foydalanuvchi referal orqali kelgan bo'lsa, refererga xabar yuborish
    if referral_id:
        referrer = await rqs.get_user()
        if referrer:
            await rqs.add_referal(referrer.chat_id)
            await message.bot.send_message(
                chat_id=referrer.chat_id,
                text=f"Sizning referal link orqali yangi foydalanuvchi ({first_name}) qo'shildi!"
            )

    # Foydalanuvchini xush kelibsiz xabar bilan kutib olish
    await message.answer(f"Assalomu alaykum, {first_name}! Botdan foydalanishingiz mumkin.", reply_markup=user_keyboard)

@router.message(lambda message: message.text == "Referallar soni")
async def show_referrals(message: types.Message):
    if not await message_for_channel(message):
        return
    user_id = message.from_user.id
    referral_count = await rqs.get_user_referrals_count(user_id)
    await message.answer(f"Siz hozirgacha {referral_count} ta odamni taklif qilgansiz.")

@router.message(lambda message: message.text == "Referal havolasini olish")
async def referral_link(message: types.Message):
    if not await message_for_channel(message):
        return
    user_id = message.from_user.id
    await message.answer(f"Sizning referal havolangiz:\n https://t.me/kariymulloh_referalbot?start=r_{user_id}")

@router.message(lambda message: message.text == "TOP 50 Referlar")
async def show_top_referrers(message: types.Message):
    if not await message_for_channel(message):
        return
    top_referrers = await rqs.get_top_referrers()
    response = "TOP 50 Referlar:\n" + "\n".join(
        [f"{idx + 1}. {user.first_name}  -  {user.referals_count} ta" for idx, user in enumerate(top_referrers)]
    )
    await message.answer(response)

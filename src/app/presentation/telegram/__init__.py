from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

reply_markup = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Cancel")]], resize_keyboard=True
)

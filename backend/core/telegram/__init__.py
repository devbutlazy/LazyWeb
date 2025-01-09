from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

image_reply_markup = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Cancel"), KeyboardButton(text="Skip")]],
    resize_keyboard=True,
)
cancel_reply_markup = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Cancel")]],
    resize_keyboard=True,
)
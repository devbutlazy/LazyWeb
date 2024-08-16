from aiogram import Router
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

router = Router()

reply_markup = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Cancel")]], resize_keyboard=True
)

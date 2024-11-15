from aiogram.filters.callback_data import CallbackData


class RemovePostCallback(CallbackData, prefix="remove_post"):
    id: int

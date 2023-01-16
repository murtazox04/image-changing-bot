from aiogram.dispatcher.filters.state import StatesGroup, State


class GetState(StatesGroup):
    audio_id = State()
    photo = State()

from aiogram.dispatcher.filters.state import StatesGroup, State


class GetState(StatesGroup):
    audio_id = State()
    performer = State()
    audio_title = State()
    file_name = State()
    photo = State()

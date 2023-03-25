from aiogram.dispatcher.filters.state import State, StatesGroup

class Films(StatesGroup):
    by_search = State()
    load_video = State()
    load_photo = State()
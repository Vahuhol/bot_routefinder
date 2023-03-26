from aiogram.dispatcher.filters.state import StatesGroup, State


class LocationStates(StatesGroup):
    getting_start_location = State()
    getting_end_location = State()

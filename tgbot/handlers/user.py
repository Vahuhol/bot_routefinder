from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InputFile

from ..keyboards.inline import markup_location_requests

from ..misc.states import LocationStates

from utils.map_worker import MapWorker


async def user_start(message: Message, state: FSMContext):
    await state.set_state(LocationStates.getting_start_location.state)
    await message.reply("Hello, user!", reply_markup=markup_location_requests)


async def get_user_location(message: Message, state: FSMContext):
    await state.update_data(start_location=message.location)
    await state.set_state(LocationStates.getting_end_location)
    await message.reply('Введите конечный адрес')


async def make_route(message: Message, state: FSMContext):
    state_data = await state.get_data()
    end_location = message.text
    map_worker = MapWorker(state_data.get('start_location'), end_location)
    plot = map_worker.get_plot()
    map_worker.save_plot_as_image(plot)
    await message.answer_photo(InputFile('res/map.png'))
    await state.set_state(LocationStates.getting_start_location)


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=['start'], state='*')
    dp.register_message_handler(get_user_location, content_types=['location'],
                                state=LocationStates.getting_start_location)
    dp.register_message_handler(make_route, content_types=['text'], state=LocationStates.getting_end_location)

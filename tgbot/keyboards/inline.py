from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# markup_location_requests = InlineKeyboardMarkup(resize_keyboard=True)
# markup_location_requests.add(InlineKeyboardButton('Построить маршрут', request_location=True))

markup_location_requests = ReplyKeyboardMarkup(resize_keyboard=True)
markup_location_requests.add(KeyboardButton('Построить маршрут', request_location=True))

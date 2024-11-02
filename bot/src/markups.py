

import statistics
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from const import markups, analytics_markups, lang_markups, level_markups
# markups
profile = KeyboardButton(text=markups['profile'])
logout = KeyboardButton(text=markups['logout']) 
login = KeyboardButton(text=markups['login'])
speech_book = KeyboardButton(text=markups['speech/book'])
statistics = KeyboardButton(text=markups['statistics'])
analytics = KeyboardButton(text=markups['analytics'])
summarize = KeyboardButton(text=markups['summarize'])
# Создаем клавиатуру для неавторизованного пользователя
user_markup = ReplyKeyboardMarkup(keyboard=[[login], [speech_book], [summarize]], resize_keyboard=True)

# Создаем клавиатуру для авторизованного пользователя


auth_user_markup = ReplyKeyboardMarkup(keyboard=[[speech_book, profile], [statistics, analytics], [summarize, logout]], resize_keyboard=True)


analytics_markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=i[1], callback_data=i[0])] for i in analytics_markups.items()])

level_markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=i[1], callback_data=i[0])] for i in level_markups.items()])

lang_markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=i[1], callback_data=i[0])] for i in lang_markups.items()])




from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from const import markups

profile = KeyboardButton(text=markups['profile'])
logout = KeyboardButton(text=markups['logout']) 
feedback = KeyboardButton(text=markups['feedback'])
login = KeyboardButton(text=markups['login'])
user_markup = ReplyKeyboardMarkup(keyboard=[[feedback, login]], resize_keyboard=True)
auth_user_markup = ReplyKeyboardMarkup(keyboard=[[profile, logout, feedback]], resize_keyboard=True)
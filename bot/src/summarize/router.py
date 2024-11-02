
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.src.utils.get_markup import get_markup
from markups import markups, user_markup, lang_markups, level_markups
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from markups import lang_markup, level_markup
from server.src.ai_connect import model_sum, tokenizer, device


class SummarizeState(StatesGroup):
    level = State()
    lang = State()
    text = State()




router = Router(name="summarize")


async def sum_text(text:str, level:str, lang:str):
    prefix = f"{level} {lang}:"
    src_text = prefix + text
    input_ids = tokenizer(src_text, return_tensors="pt")

    generated_tokens = model_sum.generate(**input_ids.to(device))

    result = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
    return result[0]

level = None
lang = None
@router.message(F.text == markups['summarize'])
async def summarize_handler(msg: Message, session: AsyncSession, state: FSMContext): 
	
	await state.set_state(SummarizeState.level)
	await msg.answer(text="Выберите уровень сжатия", reply_markup=level_markup)
     


@router.callback_query(lambda c: c.data in level_markups)
async def analytics_graph_handler(callback_query: CallbackQuery, session: AsyncSession, state: FSMContext):
    selected_option = callback_query.data 

    # Логика обработки в зависимости от выбранной кнопки
    if level_markups[selected_option]:
        await state.set_data({'level': selected_option})
        await state.set_state(SummarizeState.lang)
        await callback_query.message.answer(text="Выберите язык сжатия", reply_markup=lang_markup)
    

    # Подтверждаем получение callback
    await callback_query.answer()



@router.callback_query(lambda c: c.data in lang_markups)
async def analytics_graph_handler(callback_query: CallbackQuery, _: AsyncSession, state: FSMContext):
    selected_option = callback_query.data 

    # Логика обработки в зависимости от выбранной кнопки
    if lang_markups[selected_option]:
		
        await state.set_data({'lang': selected_option})
        await state.set_state(SummarizeState.text)	
        await callback_query.message.answer(text="Введите текст для сжатия", reply_markup=user_markup)
    

    # Подтверждаем получение callback
    await callback_query.answer()



@router.message(SummarizeState.text)
async def summarize_text(msg: Message, session: AsyncSession, state: FSMContext):	
     
	text = msg.text
	if len(text) < 350: 
		return await msg.answer(text="Текст слишком короткий, пожалуйста, введите больше текста")
	

	# data = await state.get_data()
	new_text = await sum_text(text, level, lang)	
	markup = await get_markup(msg.from_user.id, session)
	await msg.answer(text="Сжатый текст:")
	await msg.answer(text=f"{new_text}", reply_markup=markup)
	await state.clear()

  
	





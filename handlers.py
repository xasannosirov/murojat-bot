import os
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from database import save_appeal, get_appeals, get_user, save_language, update_user
from utils import get_language

class Form(StatesGroup):
    language = State()
    contact = State()
    appeal_text = State()
    file_upload = State()

languages = {"UZ": "O'zbek", "RU": "Русский", "EN": "English"}

start_markup = ReplyKeyboardMarkup(resize_keyboard=True).row(
    KeyboardButton("O'zbek"), KeyboardButton("Русский"), KeyboardButton("English")
)

def get_main_menu_markup(language_code:str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(resize_keyboard=True).row(
        KeyboardButton(get_language("Write an appeal", language_code)),
        KeyboardButton(get_language("My appeals", language_code)),
    )

bot = None

def set_bot(bot_instance):
    global bot
    bot = bot_instance

async def cmd_start(message: types.Message):
    user = get_user(message.from_user.id)
    if user:
        await message.answer(get_language("Main menu", user['language']), reply_markup=get_main_menu_markup(user['language']))
    else:
        await message.answer("Tilni tanlang:", reply_markup=start_markup)
        await Form.language.set()

async def process_language(message: types.Message, state: FSMContext):
    if message.text not in languages.values():
        await message.answer("Iltimos, tilni tanlang.")
        return

    language_code = list(languages.keys())[list(languages.values()).index(message.text)]
    await state.update_data(language=language_code)

    save_language(user_id=message.from_user.id, language=language_code)

    get_language("Share contact", language_code)
    contact_button = KeyboardButton(get_language("Share contact", language_code), request_contact=True)
    contact_markup = ReplyKeyboardMarkup(resize_keyboard=True).add(contact_button)
    await message.answer(get_language("Please share your contact details", language_code), reply_markup=contact_markup)
    await Form.next()

async def process_contact(message: types.Message, state: FSMContext):
    user = get_user(message.from_user.id)
    if not message.contact:
        await message.answer(get_language("Please share your contact details", user['language']))
        return

    update_user(
        user_id=message.from_user.id,
        first_name=message.contact.first_name,
        last_name=message.contact.last_name,
        username=message.from_user.username,
        phone_number=message.contact.phone_number
    )

    await message.answer(get_language("For your appeals", user['language']), reply_markup=get_main_menu_markup(user['language']))
    await state.finish()

async def cmd_appeal(message: types.Message):
    user = get_user(message.from_user.id)
    await message.answer(get_language("Write your appeal", user['language']))
    await Form.appeal_text.set()

async def process_appeal_text(message: types.Message, state: FSMContext):
    user = get_user(message.from_user.id)
    await state.update_data(appeal_text=message.text)
    file_option = ReplyKeyboardMarkup(resize_keyboard=True).row(
        KeyboardButton(get_language("Upload file", user['language'])), KeyboardButton("-")
    )
    await message.answer(get_language("Upload file or press '-'", user['language']), reply_markup=file_option)
    await Form.file_upload.set()

async def process_file_upload(message: types.Message, state: FSMContext):
    data = await state.get_data()
    appeal_text = data['appeal_text']
    user_id = message.from_user.id
    user = get_user(user_id)

    if message.text == get_language("Upload file", user['language']):
        await message.answer(get_language("Please upload the file", user['language']))
        return
    elif message.text == "-":
        save_appeal(user_id, appeal_text)
        await message.answer(get_language("Your appeal has been saved", user['language']))
        await message.answer(get_language("For your appeals", user['language']), reply_markup=get_main_menu_markup(user['language']))
        await state.finish()
    else:
        await message.answer(get_language("Upload file or press '-'", user['language']))

async def process_file(message: types.Message, state: FSMContext):
    user = get_user(message.from_user.id)
    if not message.document:
        await message.answer(get_language("Please upload the file", user['language']))
        return

    data = await state.get_data()
    appeal_text = data['appeal_text']
    user_id = message.from_user.id

    file_id = message.document.file_id
    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path
    split_tup = os.path.splitext(message.document.file_name)
    file_name = message.document.file_unique_id+split_tup[1]

    await bot.download_file(file_path, f"files/{file_name}")

    save_appeal(user_id, appeal_text, file_url=file_name)
    await message.answer(get_language("Your appeal has been saved", user['language']))
    await message.answer(get_language("For your appeals", user['language']), reply_markup=get_main_menu_markup(user['language']))
    await state.finish()

async def cmd_my_appeals(message: types.Message):
    user = get_user(message.from_user.id)
    appeals = get_appeals(message.from_user.id)
    if not appeals:
        await message.answer(get_language("You have no appeals", user['language']))
        return

    for appeal in appeals:
        appeal_text = appeal['appeal_text']
        file_url = appeal['file_url']

        if file_url:
            file_path = f"./files/{file_url}"
            try:
                with open(file_path, 'rb') as file:
                    await message.answer_document(document=file, caption=appeal_text)
            except FileNotFoundError:
                pass
        else:
            await message.answer(appeal_text)

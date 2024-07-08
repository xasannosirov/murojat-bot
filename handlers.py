import os
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from database import save_user, save_appeal, get_appeals, get_user

class Form(StatesGroup):
    language = State()
    contact = State()
    appeal_text = State()
    file_upload = State()

languages = {"UZ": "O'zbek", "RU": "Русский", "EN": "English"}

start_markup = ReplyKeyboardMarkup(resize_keyboard=True).row(
    KeyboardButton("O'zbek"), KeyboardButton("Русский"), KeyboardButton("English")
)

main_menu_markup = ReplyKeyboardMarkup(resize_keyboard=True).row(
    KeyboardButton("Murojat yozish"), KeyboardButton("Mening murojatlarim")
)

bot = None

def set_bot(bot_instance):
    global bot
    bot = bot_instance

async def cmd_start(message: types.Message):
    user = get_user(message.from_user.id)
    if user:
        main_menu = ReplyKeyboardMarkup(resize_keyboard=True).row(
            KeyboardButton("Murojat yozish"), KeyboardButton("Mening murojatlarim")
        )
        await message.answer("Asosiy menyu", reply_markup=main_menu)
    else:
        await message.answer("Tilni tanlang:", reply_markup=start_markup)
        await Form.language.set()

async def process_language(message: types.Message, state: FSMContext):
    if message.text not in languages.values():
        await message.answer("Iltimos, tilni tanlang.")
        return

    language_code = list(languages.keys())[list(languages.values()).index(message.text)]
    await state.update_data(language=language_code)

    contact_button = KeyboardButton('Kontakt ulashish', request_contact=True)
    contact_markup = ReplyKeyboardMarkup(resize_keyboard=True).add(contact_button)
    await message.answer("Iltimos, kontakt ma'lumotlaringizni ulashing.", reply_markup=contact_markup)
    await Form.next()

async def process_contact(message: types.Message, state: FSMContext):
    if not message.contact:
        await message.answer("Iltimos, kontakt ma'lumotlaringizni ulashing.")
        return

    data = await state.get_data()
    language = data['language']

    save_user(
        user_id=message.from_user.id,
        first_name=message.contact.first_name,
        last_name=message.contact.last_name,
        username=message.from_user.username,
        phone_number=message.contact.phone_number,
        language=language
    )

    await message.answer("Sizning murojatlariz uchun:", reply_markup=main_menu_markup)
    await state.finish()

async def cmd_appeal(message: types.Message, state: FSMContext):
    await message.answer("Murojaatingizni yozing:")
    await Form.appeal_text.set()

async def process_appeal_text(message: types.Message, state: FSMContext):
    await state.update_data(appeal_text=message.text)
    file_option = ReplyKeyboardMarkup(resize_keyboard=True).row(
        KeyboardButton("File yuklash"), KeyboardButton("-")
    )
    await message.answer("File yuklashingiz mumkin yoki '-' belgisini bosing:", reply_markup=file_option)
    await Form.file_upload.set()

async def process_file_upload(message: types.Message, state: FSMContext):
    data = await state.get_data()
    appeal_text = data['appeal_text']
    user_id = message.from_user.id

    if message.text == "File yuklash":
        await message.answer("Iltimos, faylni yuklang.")
        return
    elif message.text == "-":
        save_appeal(user_id, appeal_text)
        await message.answer("Murojaatingiz saqlandi.")
        await message.answer("Sizning murojatlariz uchun:", reply_markup=main_menu_markup)
        await state.finish()
    else:
        await message.answer("Iltimos, file yuklang yoki '-' ni bosing.")

async def process_file(message: types.Message, state: FSMContext):
    if not message.document:
        await message.answer("Iltimos, fayl yuklang.")
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
    await message.answer("Murojaatingiz saqlandi.")
    await message.answer("Sizning murojatlariz uchun:", reply_markup=main_menu_markup)
    await state.finish()

async def cmd_my_appeals(message: types.Message):
    appeals = get_appeals(message.from_user.id)
    if not appeals:
        await message.answer("Sizda murojatlar yo'q.")
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
                await message.answer(f"Fayl topilmadi: {file_url}")
        else:
            await message.answer(appeal_text)

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.states import Search
from keyboards.builders import cancel_button

router = Router()

group_id = -1002247407329


@router.message(F.video)
async def file_id(message: Message):
    if message.chat.id == group_id:  # замените ADMIN_ID на ID администратора
        # Функция для загрузки данных из файла
        try:
            with open('data/kodlar.txt', 'r') as f:
                video_ids = [int(line.rstrip()) for line in f]
        except FileNotFoundError:
            video_ids = []
        video_id = message.message_id
        video_ids.append(video_id)
        await message.reply(f"Ko'd: {video_id}")
        save_video_ids(video_id)


@router.message(F.text == "🔎 Izlash")
async def file_id(message: Message, state: FSMContext):
    await message.answer("✧ Kodni yuboring", reply_markup=cancel_button())
    await state.set_state(Search.code)


# Функция для сохранения данных в файл
def save_video_ids(vid_id):
    with open('data/kodlar.txt', 'a') as f:  # Используем 'a' для добавления новых строк в файл
        f.write(f"{vid_id}\n")

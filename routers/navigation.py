from aiogram import Router, F

from aiogram.types import Message
from keyboards.builders import admin_button, menu_button
router = Router()


@router.message(F.text == "🔙 Ortga")
async def prev(message: Message):
    with open('data/adminlar.txt', 'r') as f:
        admin_id = [int(line.rstrip()) for line in f]
    if message.chat.id in admin_id:
        await message.answer("✧ Menyu", reply_markup=admin_button())
    else:
        await message.answer("✧ Menyu", reply_markup=menu_button())

from aiogram import Router

from aiogram.types import Message
from aiogram.filters import Command

from keyboards.builders import admin_button, menu_button

router = Router()

admin_id = []


@router.message(Command("start"))
async def start(message: Message):
    user_w(message.from_user.id)
    with open('data/adminlar.txt', 'r') as f:
        admin_id = [int(line.rstrip()) for line in f]
    if message.from_user.id in admin_id:
        await message.answer("❖ Admin", reply_markup=admin_button())
    else:
        await message.answer("❖ User", reply_markup=menu_button())


@router.message(Command("user_id"))
async def start(message: Message):
    await message.answer(f"❖ {message.from_user.id}")


@router.message(Command("group_id"))
async def start(message: Message):
    await message.answer(f"❖ {message.chat.id}")


@router.message(Command("res"))
async def res_start(message: Message):
    global admin_id
    await message.answer(f"❖ Tizm tiklandi")
    with open('data/adminlar.txt', 'r') as f:
        admin_id = [int(line.rstrip()) for line in f]


def get_user_ids():
    with open('data/users.txt', 'r') as f:
        return [line.strip() for line in f]


def count_users():
    user_ids = get_user_ids()
    return len(user_ids)


@router.message(Command("users"))
async def count_users_command(message: Message):
    user_count = count_users()
    await message.answer(f"Foydalanuvchilar soni: {user_count} 👥")


def user_w(user_id):
    with open('data/users.txt', 'a') as f:  # Используем 'a' для добавления новых строк в файл
        f.write(f"{user_id}\n")

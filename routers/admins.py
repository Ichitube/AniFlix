from aiogram import Router, F

from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext


from states.states import Admin
from keyboards.builders import admin_button, menu_button, cancel_button, inline_builder

router = Router()


@router.message(F.text == "👤 Admin")
@router.callback_query(F.data == "main_page")
async def main_menu(message: Message | CallbackQuery):
    pattern = dict(
            text=f"✧ 👤 Adminlar bo'limi",
            parse_mode=ParseMode.HTML,
            reply_markup=inline_builder(
                ["👤 Admin ➕", "👤 Admin ➖"],
                ["add_admin", "del_admin"],
                row_width=[2])
        )
    await message.answer(**pattern)


@router.callback_query(F.data == "add_admin")
async def main_menu(message: Message | CallbackQuery, state: FSMContext):
    pattern = dict(
        text=f"✧ ➕ user_id ni yuboring",
        parse_mode=ParseMode.HTML,
        reply_markup=cancel_button()
    )
    await message.message.answer(**pattern)
    await state.set_state(Admin.uid)


@router.message(Admin.uid)
async def add_admin(message: Message | CallbackQuery, state: FSMContext):
    with open('data/adminlar.txt', 'r') as f:
        admin_id = [int(line.rstrip()) for line in f]
    if message.text == "🔙 Ortga":
        await state.clear()
        if message.chat.id in admin_id:
            await message.answer("✧ Menyu", reply_markup=admin_button())
        else:
            await message.answer("✧ Menyu", reply_markup=menu_button())
    uid = int(message.text)  # Исправлено преобразование ID
    save_admin_id(uid)
    await message.answer("✧ Admin qo'shildi")
    await state.clear()  # Сброс состояния после добавления


@router.callback_query(F.data == "del_admin")
async def main_menu(message: Message | CallbackQuery, state: FSMContext):
    pattern = dict(
        text=f"✧ ➖ user_id ni yuboring",
        parse_mode=ParseMode.HTML,
        reply_markup=cancel_button()
    )
    await message.message.answer(**pattern)
    await state.set_state(Admin.min)


@router.message(Admin.min)
async def add_admin(message: Message | CallbackQuery, state: FSMContext):
    with open('data/adminlar.txt', 'r') as f:
        admin_id = [int(line.rstrip()) for line in f]
    if message.text == "🔙 Ortga":
        await state.clear()
        if message.chat.id in admin_id:
            await message.answer("✧ Menyu", reply_markup=admin_button())
        else:
            await message.answer("✧ Menyu", reply_markup=menu_button())
    uid = int(message.text)  # Исправлено преобразование ID
    del_admin_id(uid)
    await message.answer("✧ Admin o'chirildi")
    await state.clear()  # Сброс состояния после добавления


def save_admin_id(uid):
    with open('data/adminlar.txt', 'a') as f:  # Используем 'a' для добавления новых строк в файл
        f.write(f"{uid}\n")


def del_admin_id(uid):
    uid = str(uid)  # Приведение uid к строке, если он был передан как число
    try:
        with open('data/adminlar.txt', 'r') as f:
            lines = f.readlines()  # Чтение всех строк из файла

        with open('data/adminlar.txt', 'w') as f:
            for line in lines:
                if line.strip() != uid:  # Сравниваем без пробелов в начале и конце строки
                    f.write(line)  # Перезаписываем все строки, кроме той, что нужно удалить
    except FileNotFoundError:
        # Если файл не найден, ничего не делаем, так как удалять нечего
        pass

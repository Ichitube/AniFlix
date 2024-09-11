import json
from aiogram import Router, F

from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext


from states.states import Channel
from routers.mess import check_user_subscriptions, load_channels
from keyboards.builders import admin_button, menu_button, cancel_button, bd, inline_builder

# Путь к файлу, где будут храниться каналы
CHANNELS_FILE = 'data/channels.json'
router = Router()

group_id = -1002247407329


@router.message(F.text == "🔗 Kanal")
async def main_menu(message: Message | CallbackQuery):
    pattern = dict(
            text=f"✧ 🔗 Referal Kanallar ro'yxati"
                 f"\n\n{list(load_channels().keys())}",
            parse_mode=ParseMode.HTML,
            reply_markup=inline_builder(
                ["📣 Kanal ➕", "📣 Kanal ➖"],
                ["add_channel", "del_channel"],
                row_width=[2])
        )
    await message.answer(**pattern)


@router.callback_query(F.data == "add_channel")
async def main_menu(message: Message | CallbackQuery, state: FSMContext):
    pattern = dict(
        text=f"✧ Kanal nomini yuboring",
        reply_markup=cancel_button()
    )
    await message.message.answer(**pattern)
    await state.set_state(Channel.name)


@router.message(Channel.name)
async def add_admin(message: Message| CallbackQuery, state: FSMContext):
    await state.update_data(name=message.text)
    with open('data/adminlar.txt', 'r') as f:
        admin_id = [int(line.rstrip()) for line in f]
    if message.text == "🔙 Ortga":
        await state.clear()
        if message.chat.id in admin_id:
            await message.answer("✧ Menyu", reply_markup=admin_button())
        else:
            await message.answer("✧ Menyu", reply_markup=menu_button())
    else:
        await message.answer("✧ Linkni yuboring ✔️")
        await state.set_state(Channel.link)


@router.message(Channel.link)
async def add_admin(message: Message| CallbackQuery, state: FSMContext):
    await state.update_data(link=message.text)
    with open('data/adminlar.txt', 'r') as f:
        admin_id = [int(line.rstrip()) for line in f]
    if message.text == "🔙 Ortga":
        await state.clear()
        if message.chat.id in admin_id:
            await message.answer("✧ Menyu", reply_markup=admin_button())
        else:
            await message.answer("✧ Menyu", reply_markup=menu_button())
    else:
        data = await state.get_data()
        add_channel(data['name'], data['link'])
        await message.answer("✧ Kanal qo'shildi ✔️")
        await state.clear()


@router.callback_query(F.data == "del_channel")
async def main_menu(message: Message | CallbackQuery, state: FSMContext):
    pattern = dict(
        text=f"✧ Kanal nomini yuboring",
        reply_markup=cancel_button()
    )
    await message.message.answer(**pattern)
    await state.set_state(Channel.dell)


@router.message(Channel.dell)
async def add_admin(message: Message | CallbackQuery, state: FSMContext):
    name = message.text
    with open('data/adminlar.txt', 'r') as f:
        admin_id = [int(line.rstrip()) for line in f]
    if message.text == "🔙 Ortga":
        await state.clear()
        if message.chat.id in admin_id:
            await message.answer("✧ Menyu", reply_markup=admin_button())
        else:
            await message.answer("✧ Menyu", reply_markup=menu_button())
    else:
        if remove_channel(name):
            await message.answer(f"✧ Kanal '{name}' O'chirildi ✔️")
        else:
            await message.answer(f"Kanal '{name}' topilmadi ✖️")
        await state.clear()


# Команда для добавления канала
@router.message(Command("add_channel"))
async def add_channel_command(message: Message):
    args = message.text.split(maxsplit=2)
    if len(args) != 3:
        await message.answer("Используйте команду в формате: /add_channel <название> <ссылка>")
        return

    name = args[1]
    link = args[2]
    add_channel(name, link)
    await message.answer(f"Канал '{name}' успешно добавлен.")


# Команда для удаления канала
@router.message(Command("remove_channel"))
async def remove_channel_command(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) != 2:
        await message.answer("Используйте команду в формате: /remove_channel <название>")
        return

    name = args[1]
    if remove_channel(name):
        await message.answer(f"Канал '{name}' успешно удален.")
    else:
        await message.answer(f"Канал '{name}' не найден.")


# Функция для сохранения каналов в файл
def save_channels(channels):
    with open(CHANNELS_FILE, 'w') as f:
        json.dump(channels, f, indent=4)


# Функция для добавления канала
def add_channel(name, link):
    channels = load_channels()
    channels[name] = link
    save_channels(channels)


# Функция для удаления канала
def remove_channel(name):
    channels = load_channels()
    if name in channels:
        del channels[name]
        save_channels(channels)
        return True
    return False

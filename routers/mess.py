import json
from aiogram import Router, F

from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from keyboards.builders import inline_builder, cancel_button, bot_link, admin_button, menu_button, ch_builder
from states.states import Mess, Search
from aiogram.fsm.context import FSMContext
from main import bot

router = Router()

group_id = -1002247407329
CHANNELS_FILE = 'data/channels.json'


@router.message(F.text == "?? Habar")
async def main_menu(message: Message):
    pattern = dict(
            text=f"?? Habar yoki post yuborish",
            parse_mode=ParseMode.HTML,
            reply_markup=inline_builder(
                ["?? Post", "?? Habar"],
                ["mes_channel", "mes_users"],
                row_width=[2])
        )
    await message.answer(**pattern)


@router.callback_query(F.data == "mes_channel")
async def main_menu(message: Message | CallbackQuery, state: FSMContext):
    await message.message.answer("?? Postnni yuboring", reply_markup=cancel_button())
    await state.set_state(Mess.post)


@router.callback_query(F.data == "mes_users")
async def main_menu(message: Message | CallbackQuery, state: FSMContext):
    pattern = dict(
        text=f"? ?? Habarni yuboring",
        reply_markup=cancel_button()
    )
    await message.message.answer(**pattern)
    await state.set_state(Mess.msg)


@router.message(Mess.post)
async def add_admin(message: Message| CallbackQuery, state: FSMContext):
    with open('data/adminlar.txt', 'r') as f:
        admin_id = [int(line.rstrip()) for line in f]
    if message.text == "?? Ortga":
        await state.clear()
        if message.chat.id in admin_id:
            await message.answer("? Menyu", reply_markup=admin_button())
        else:
            await message.answer("? Menyu", reply_markup=menu_button())
    else:
        await bot.send_message(
            chat_id=-1002210789769,
            text=message.text,
            reply_markup=bot_link()
        )
        await message.answer("? Habar yuborildi ??")


@router.message(Mess.msg)
async def add_admin(message: Message | CallbackQuery, state: FSMContext):
    with open('data/adminlar.txt', 'r') as f:
        admin_id = [int(line.rstrip()) for line in f]
    if message.text == "?? Ortga":
        await state.clear()
        if message.chat.id in admin_id:
            await message.answer("? Menyu")
        else:
            await message.answer("? Menyu")
    else:
        await send_message_to_users(message.text)
        await message.answer("? Habar yuborildi ??")


def save_admin_id(uid):
    with open('data/adminlar.txt', 'a') as f:  # Используем 'a' для добавления новых строк в файл
        f.write(f"{uid}\n")


@router.message(Search.code)
async def res_vid(message: Message, state: FSMContext):
    # Функция для загрузки данных из файла
    try:
        with open('data/kodlar.txt', 'r') as f:
            video_ids = [int(line.rstrip()) for line in f]
    except FileNotFoundError:
        video_ids = []
    if message.text == "?? Ortga":
        with open('data/adminlar.txt', 'r') as f:
            admin_id = [int(line.rstrip()) for line in f]
        await state.clear()
        if message.chat.id in admin_id:
            await message.answer("? Menyu", reply_markup=admin_button())
        else:
            await message.answer("? Menyu", reply_markup=menu_button())
    else:
        user_id = message.from_user.id
        not_subscribed = await check_user_subscriptions(user_id)

        if not_subscribed:
            await message.answer(f"? ?? Botdan Foydalanish uchun quyidagi kanallarga a'zo bo'lishingiz kerak:",
                                 reply_markup=ch_builder(list(load_channels().keys()), list(load_channels().values()), row_width=1))
        else:
            try:
                if int(message.text) in video_ids:
                    index = video_ids.index(int(message.text))
                    video = video_ids[index]
                    await bot.copy_message(message.chat.id, group_id, video)
                else:
                    await message.answer("? Bunday kod mavjud emas!")
            except:
                await message.answer("? Noto'g'ri kod!")


def get_user_ids():
    with open('data/users.txt', 'r') as f:
        return [line.strip() for line in f]


# Функция для отправки сообщения каждому пользователю
async def send_message_to_users(text):
    user_ids = get_user_ids()
    for user_id in user_ids:
        try:
            await bot.send_message(chat_id=user_id, text=text)
        except Exception as e:
            print(f"Foydalanuvchi {user_id}: {e} habarni olmadi")


# Функция для загрузки каналов из файла
def load_channels():
    try:
        with open(CHANNELS_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}


async def check_user_subscriptions(user_id: int):
    channels = load_channels()
    not_subscribed_channels = []

    for name, link in channels.items():
        channel_username = link.replace("https://t.me/", "@")
        member = await bot.get_chat_member(chat_id=channel_username, user_id=user_id)
        if member.status not in ["member", "administrator", "creator"]:
            not_subscribed_channels.append(name)

    return not_subscribed_channels
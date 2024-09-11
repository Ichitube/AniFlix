from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import (ReplyKeyboardBuilder, InlineKeyboardBuilder,
                                    InlineKeyboardMarkup, ReplyKeyboardMarkup)


def bd() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='Chat 📀', url='https://t.me/animevideola')
    return builder.as_markup()


def bot_link() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Ko'rish", url='https://t.me/AnilandUzbot?start=start')
    return builder.as_markup()


def admin_button():
    kb = [
        [
            KeyboardButton(text='🔎 Izlash'),
        ],
        [
            KeyboardButton(text='📀 Video'),
            KeyboardButton(text='🔗 Kanal')
        ],
        [
            KeyboardButton(text='📢 Habar'),
            KeyboardButton(text='👤 Admin')
        ]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder='AniLand Admin'
    )
    return keyboard


def menu_button():
    kb = [
        [
            KeyboardButton(text='🔎 Izlash'),
        ]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder='AniLand'
    )
    return keyboard


def cancel_button():
    kb = [
        [
            KeyboardButton(text='🔙 Ortga'),
        ]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )
    return keyboard


def inline_builder(
    text: str | list[str],
    callback_data: str | list[str],
    row_width: int | list[int] = 2,
    **kwargs
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if isinstance(text, str):
        text = [text]
    if isinstance(callback_data, str):
        callback_data = [callback_data]
    if isinstance(row_width, int):
        row_width = [row_width]

    [
        builder.button(text=item, callback_data=cb)
        for item, cb in zip(text, callback_data)
    ]

    builder.adjust(*row_width)
    return builder.as_markup(**kwargs)


def ch_builder(
    text: str | list[str],
    callback_data: str | list[str],
    row_width: int | list[int] = 2,
    **kwargs
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if isinstance(text, str):
        text = [text]
    if isinstance(callback_data, str):
        callback_data = [callback_data]
    if isinstance(row_width, int):
        row_width = [row_width]

    [
        builder.button(text=f'📣 {item}', url=cb)
        for item, cb in zip(text, callback_data)
    ]

    builder.adjust(*row_width)
    return builder.as_markup(**kwargs)


def reply_builder(
    text: str | list[str],
    row_width: int | list[int] = 2,
    **kwargs
) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    text = [text] if isinstance(text, str) else text
    row_width = [row_width] if isinstance(row_width, int) else row_width

    [
        builder.button(text=item)
        for item in text
    ]

    builder.adjust(*row_width)
    return builder.as_markup(resize_keyboard=True, **kwargs)

from aiogram.fsm.state import State, StatesGroup


class Search(StatesGroup):
    code = State()


class Channel(StatesGroup):
    name = State()
    link = State()
    dell = State()


class Mess(StatesGroup):
    msg = State()
    post = State()


class Admin(StatesGroup):
    uid = State()
    min = State()

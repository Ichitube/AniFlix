import logging, asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

ADMIN_ID = 6462809130
video_ids = []


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Объект бота
bot = Bot(token="6904548902:AAG44Ny4Yvf15O9VOhHEnMYTKleSg1W0pUM")

# Диспетчер
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Kodni yuboring")

@dp.message(F.text.lower() != None)
async def without_puree(message: Message):
    if int(message.text) in video_ids:
        index = video_ids.index(int(message.text))
        video = video_ids[index]
        await bot.copy_message(message.chat.id, ADMIN_ID, video)

#download video


@dp.message(F.video)
async def video_handler(message: Message):
    global video_ids
    if message.from_user.id == ADMIN_ID:  # замените ADMIN_ID на ID администратора
        video_id = message.message_id
        video_ids.append(video_id)
        await message.reply(f"Ko'd: {video_id}")
        with open('data/kodlar.txt', 'w') as f:
            for item in video_ids:
                f.write("%s\n" % item)
    else:
        await message.answer("Siz admin emassiz!")

# Запуск процесса поллинга новых апдейтов
async def main():
    global video_ids
    try:
        with open('data/kodlar.txt', 'r') as f:
            video_ids = [int(line.rstrip()) for line in f]
    except FileNotFoundError:
        video_ids = []
    await dp.start_polling(bot)
#end 3


if __name__ == "__main__":
    asyncio.run(main())

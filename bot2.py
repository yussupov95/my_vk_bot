from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text

# Вставь сюда свой новый токен
TOKEN = "vk1.a.IShdbvc7y-WNl-laMuw1g-vYEwLHjNk-nPqHZSsPbjC0Ul-dYBVjPyeur0z1i4L5r-XARvPy3p38cedqN38bFvUKqM-uRf8F8AOlJcsqe5r30NWWxep87JyZOw8xwLXXjtr5VDkrm34oo8Doznrqh3K-CdPhUd4ymOI-sjYh47PC4gisZckSK8SOFG-7nzxyBofyRfk9PUm5yaFsWVRFsQ"

bot = Bot(token=TOKEN)

def get_keyboard():
    keyboard = Keyboard(one_time=False, inline=False)
    keyboard.add(Text("Начать"), color=KeyboardButtonColor.POSITIVE)
    keyboard.add(Text("Техподдержка"), color=KeyboardButtonColor.SECONDARY)
    keyboard.row()
    keyboard.add(Text("Сделать ссылку"), color=KeyboardButtonColor.PRIMARY)
    return keyboard

@bot.on.message(text=["Начать", "Start", "начать", "start"])
async def start_handler(message: Message):
    await message.answer(
        "Добро пожаловать в ХостингБот! Здесь вы сможете из фото сделать ссылку.\n\n"
        "Нажми «Сделать ссылку» и отправь фото.",
        keyboard=get_keyboard()
    )

@bot.on.message(text=["Сделать ссылку", "сделать ссылку", "ссылка", "Ссылка"])
async def make_link_handler(message: Message):
    await message.answer(
        "Отправь мне фото, и я сделаю из него ссылку!",
        keyboard=get_keyboard()
    )

@bot.on.message(attachment="photo")
async def photo_handler(message: Message):
    photo = message.attachments[0].photo
    long_url = photo.sizes[-1].url
    await message.answer(
        f"📌 Ссылка на фото:\n{long_url}",
        keyboard=get_keyboard()
    )

@bot.on.message(text=["Техподдержка", "техподдержка", "поддержка"])
async def support_handler(message: Message):
    await message.answer(
        "📞 Связь с администратором: https://vk.com/yussupov95",
        keyboard=get_keyboard()
    )

@bot.on.message()
async def unknown_handler(message: Message):
    await message.answer(
        "Выбери пункт из меню 👇",
        keyboard=get_keyboard()
    )

if __name__ == "__main__":
    print("✅ Бот запущен и ждёт сообщения...")
    bot.run_forever()

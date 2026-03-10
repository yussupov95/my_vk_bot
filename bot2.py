from vkbottle.bot import Bot, Message
from vkbottle import Keyboard,
KeyboardButtonColor, Text

# ТВОЙ ТОКЕН
TOKEN =
"vk1.a.HEt17KHUp8qmk7p42fTXhpw7vx6Cu4AW5vbpROm8tWJE_0ha3WPCfGH_HfWGMFHh2G5Ep4VmKZPVqPJ7-r58qYGnHKd3W8J5Pr7Oe0bjXCQ-CJmSXjz_kxR9aqlrAStSQwOQ5ML0c2VMnCZICPTm_-qbjFDZOTnOjtGQtjYNOtJXqjq54MaEZ60XZu6JL6ZetOFOvzzIUXUEzGq1Nfm3eA"

bot = Bot(token=TOKEN)

# КЛАВИАТУРА
def get_keyboard():
    keyboard = Keyboard(one_time=False,
inline=False)
    keyboard.add(Text("Начать"),
color=KeyboardButtonColor.POSITIVE)
    keyboard.add(Text("Техподдержка"),
color=KeyboardButtonColor.SECONDARY)
    keyboard.row()
    keyboard.add(Text("Сделать ссылку"), color=KeyboardButtonColor.PRIMARY)
    return keyboard

# НАЧАТЬ
@bot.on.message(text=["Начать", "Start", "начать", "start"])
async def start_handler(message: Message):
    await message.answer(
        "Добро пожаловать в ХостингБот! Здесь вы сможете из фотки сделать ссылку для заполнения различных анкет.\n\n"
        "Доступные команды:\n"
        "🔹 Сделать ссылку - превратить фото в ссылку\n"
        "🔹 Техподдержка - связаться с администратором\n"
        "🔹 Начать - показать это сообщение",
        keyboard=get_keyboard()
    )

# СДЕЛАТЬ ССЫЛКУ
@bot.on.message(text=["Сделать ссылку", "сделать ссылку", "ссылка", "Ссылка"])
async def make_link_handler(message: Message):
    await message.answer(
        "Отправь мне фото, и я сделаю из него ссылку!",
        keyboard=get_keyboard()
    )

# ТЕХПОДДЕРЖКА
@bot.on.message(text=["Техподдержка", "техподдержка", "поддержка", "Помощь", "помощь"])
async def support_handler(message: Message):
    your_profile_link = "https://vk.com/yussupov95"
    await message.answer(
        f"📞 Связаться с поддержкой:\n"
        f"Напиши мне в личные сообщения: {your_profile_link}\n\n"
        f"Я отвечу как можно скорее!",
        keyboard=get_keyboard()
    )

# ФОТО
@bot.on.message(attachment="photo")
async def photo_handler(message: Message):
    photo = message.attachments[0].photo
    photo_url = photo.sizes[-1].url
    photo_id = f"photo{photo.owner_id}_{photo.id}"
    await message.answer(
        f"✅ Готово!\n\n"
        f"📌 Прямая ссылка:\n{photo_url}\n\n"
        f"📌 Attachment:\n{photo_id}",
        keyboard=get_keyboard()
    )

# ВСЁ ОСТАЛЬНОЕ
@bot.on.message()
async def unknown_handler(message: Message):
    await message.answer(
        "Отлично! А теперь выбери пункт, который тебе необходим",
        keyboard=get_keyboard()
    )

if __name__ == "__main__":
    print("✅ Бот запущен и ждёт сообщения...")
    bot.run_forever()

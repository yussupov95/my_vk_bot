from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text
import aiohttp
import json
import os

TOKEN = "vk1.a.IShdbvc7y-WNl-laMuw1g-vYEwLHjNk-nPqHZSsPbjC0Ul-dYBVjPyeur0z1i4L5r-XARvPy3p38cedqN38bFvUKqM-uRf8F8AOlJcsqe5r30NWWxep87JyZOw8xwLXXjtr5VDkrm34oo8Doznrqh3K-CdPhUd4ymOI-sjYh47PC4gisZckSK8SOFG-7nzxyBofyRfk9PUm5yaFsWVRFsQ"

bot = Bot(token=TOKEN)

HISTORY_FILE = "history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

history_db = load_history()

def add_link(user_id, link, link_type):
    user_id = str(user_id)
    if user_id not in history_db:
        history_db[user_id] = []
    history_db[user_id].append({"link": link, "type": link_type})
    if len(history_db[user_id]) > 5:
        history_db[user_id].pop(0)
    save_history(history_db)

async def shorten_url(long_url: str) -> str:
    try:
        async with aiohttp.ClientSession() as session:
            params = {'url': long_url}
            async with session.get('https://clck.ru/--', params=params) as resp:
                if resp.status == 200:
                    return await resp.text()
                else:
                    return long_url
    except:
        return long_url

def get_keyboard():
    keyboard = Keyboard(one_time=False, inline=False)
    keyboard.add(Text("Начать"), color=KeyboardButtonColor.POSITIVE)
    keyboard.add(Text("Техподдержка"), color=KeyboardButtonColor.SECONDARY)
    keyboard.add(Text("Помощь"), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()
    keyboard.add(Text("Сделать ссылку"), color=KeyboardButtonColor.PRIMARY)
    keyboard.add(Text("Видео ссылка"), color=KeyboardButtonColor.PRIMARY)
    keyboard.add(Text("Благотворительность"), color=KeyboardButtonColor.SECONDARY)
    keyboard.row()
    keyboard.add(Text("Мои ссылки"), color=KeyboardButtonColor.SECONDARY)
    return keyboard

@bot.on.message(text=["Начать", "Start", "начать", "start"])
async def start_handler(message: Message):
    await message.answer(
        "Добро пожаловать в ХостингБот! Здесь вы сможете из фото или видео сделать короткую ссылку.\n\n"
        "Нажми «Помощь», чтобы узнать все возможности.",
        keyboard=get_keyboard()
    )

@bot.on.message(text=["Помощь", "помощь", "help", "Help"])
async def help_handler(message: Message):
    help_text = (
        "📋 **Доступные команды**\n\n"
        "🔹 Сделать ссылку – отправь фото, получишь короткую ссылку.\n"
        "🔹 Видео ссылка – отправь видео, получишь короткую ссылку.\n"
        "🔹 Благотворительность – номер карты для поддержки.\n"
        "🔹 Мои ссылки – история последних 5 созданных ссылок.\n"
        "🔹 Техподдержка – связь с администратором.\n"
        "🔹 Начать – приветствие."
    )
    await message.answer(help_text, keyboard=get_keyboard())

@bot.on.message(text=["Благотворительность", "благотворительность", "карта", "помочь"])
async def donate_handler(message: Message):
    card_number = "2202 2081 4442 2046"  # замени на свой номер!
    await message.answer(
        f"🙏 Спасибо за поддержку!\n\n"
        f"💳 Номер карты Сбера:\n`{card_number}`\n\n"
        f"Любая сумма поможет развитию бота.",
        keyboard=get_keyboard()
    )

@bot.on.message(text=["Сделать ссылку", "сделать ссылку", "ссылка", "Ссылка"])
async def make_link_handler(message: Message):
    await message.answer(
        "Отправь мне фото, и я сделаю из него короткую ссылку!",
        keyboard=get_keyboard()
    )

@bot.on.message(text=["Видео ссылка", "видео ссылка", "видео"])
async def video_link_handler(message: Message):
    await message.answer(
        "Отправь мне видео, и я сделаю из него короткую ссылку!",
        keyboard=get_keyboard()
    )

@bot.on.message(attachment="photo")
async def photo_handler(message: Message):
    photo = message.attachments[0].photo
    long_url = photo.sizes[-1].url
    short_url = await shorten_url(long_url)
    photo_id = f"photo{photo.owner_id}_{photo.id}"
    add_link(message.from_id, short_url, "фото")
    await message.answer(
        f"✅ Готово!\n\n"
        f"📌 Короткая ссылка:\n{short_url}\n\n"
        f"📌 Attachment:\n{photo_id}",
        keyboard=get_keyboard()
    )

@bot.on.message(attachment="video")
async def video_handler(message: Message):
    video = message.attachments[0].video
    if hasattr(video, 'files') and video.files:
        long_url = video.files[0].url if video.files else None
    else:
        long_url = f"https://vk.com/video{video.owner_id}_{video.id}"
    
    if long_url:
        short_url = await shorten_url(long_url)
    else:
        short_url = "Не удалось получить ссылку"
    
    video_id = f"video{video.owner_id}_{video.id}"
    add_link(message.from_id, short_url, "видео")
    await message.answer(
        f"✅ Готово!\n\n"
        f"📌 Короткая ссылка:\n{short_url}\n\n"
        f"📌 Attachment:\n{video_id}",
        keyboard=get_keyboard()
    )

@bot.on.message(text=["Мои ссылки", "мои ссылки", "история"])
async def history_handler(message: Message):
    user_id = str(message.from_id)
    if user_id not in history_db or not history_db[user_id]:
        await message.answer("У вас пока нет сохранённых ссылок.", keyboard=get_keyboard())
        return
    
    lines = ["📜 **Ваши последние ссылки:**\n"]
    for idx, item in enumerate(history_db[user_id], 1):
        lines.append(f"{idx}. {item['type']}: {item['link']}")
    await message.answer("\n".join(lines), keyboard=get_keyboard())

@bot.on.message(text=["Техподдержка", "техподдержка", "поддержка", "Помощь", "помощь"])
async def support_handler(message: Message):
    your_profile_link = "https://vk.com/yussupov95"  # замени на свой профиль
    await message.answer(
        f"📞 Связаться с поддержкой:\n"
        f"Напиши мне в личные сообщения: {your_profile_link}\n\n"
        f"Я отвечу как можно скорее!",
        keyboard=get_keyboard()
    )

@bot.on.message()
async def unknown_handler(message: Message):
    await message.answer(
        "Отлично! А теперь выбери пункт, который тебе необходим",
        keyboard=get_keyboard()
    )

if name == "__main__":
    print("✅ Бот запущен и ждёт сообщения...")
    bot.run_forever()



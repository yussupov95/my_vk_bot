from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text
import aiohttp
import json
import os
from datetime import datetime

TOKEN = "vk1.a.IShdbvc7y-WNl-laMuw1g-vYEwLHjNk-nPqHZSsPbjC0Ul-dYBVjPyeur0z1i4L5r-XARvPy3p38cedqN38bFvUKqM-uRf8F8AOlJcsqe5r30NWWxep87JyZOw8xwLXXjtr5VDkrm34oo8Doznrqh3K-CdPhUd4ymOI-sjYh47PC4gisZckSK8SOFG-7nzxyBofyRfk9PUm5yaFsWVRFsQ"

bot = Bot(token=TOKEN)

HISTORY_FILE = "history.json"
DONATIONS_FILE = "donations.json"

ADMIN_ID = 609908758

user_menu_state = {}

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

def load_donations():
    if os.path.exists(DONATIONS_FILE):
        with open(DONATIONS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_donations(donations):
    with open(DONATIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(donations, f, ensure_ascii=False, indent=2)

donations_db = load_donations()

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

def get_main_menu():
    keyboard = Keyboard(one_time=False, inline=False)
    keyboard.add(Text("📸 Создать ссылку"), color=KeyboardButtonColor.PRIMARY)
    keyboard.add(Text("ℹ️ Инфо"), color=KeyboardButtonColor.SECONDARY)
    keyboard.row()
    keyboard.add(Text("👤 Моё"), color=KeyboardButtonColor.SECONDARY)
    return keyboard

def get_create_links_menu():
    keyboard = Keyboard(one_time=False, inline=False)
    keyboard.add(Text("🖼 Фото (обычная)"), color=KeyboardButtonColor.PRIMARY)
    keyboard.add(Text("🖼 Фото (Яндекс)"), color=KeyboardButtonColor.SECONDARY)
    keyboard.row()
    keyboard.add(Text("🎥 Видео (обычная)"), color=KeyboardButtonColor.PRIMARY)
    keyboard.add(Text("🎥 Видео (Яндекс)"), color=KeyboardButtonColor.SECONDARY)
    keyboard.row()
    keyboard.add(Text("🌐 Сайт"), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()
    keyboard.add(Text("← Назад"), color=KeyboardButtonColor.SECONDARY)
    return keyboard

def get_info_menu():
    keyboard = Keyboard(one_time=False, inline=False)
    keyboard.add(Text("📝 Отзывы"), color=KeyboardButtonColor.SECONDARY)
    keyboard.add(Text("💬 Наш чат"), color=KeyboardButtonColor.SECONDARY)
    keyboard.row()
    keyboard.add(Text("💰 Благотворительность"), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()
    keyboard.add(Text("🏆 Топ донатеров"), color=KeyboardButtonColor.SECONDARY)
    keyboard.row()
    keyboard.add(Text("← Назад"), color=KeyboardButtonColor.SECONDARY)
    return keyboard

def get_my_menu():
    keyboard = Keyboard(one_time=False, inline=False)
    keyboard.add(Text("📜 Мои ссылки"), color=KeyboardButtonColor.SECONDARY)
    keyboard.add(Text("📊 История"), color=KeyboardButtonColor.SECONDARY)
    keyboard.row()
    keyboard.add(Text("← Назад"), color=KeyboardButtonColor.SECONDARY)
    return keyboard

@bot.on.message(text=["Начать", "Start", "начать", "start"])
async def start_handler(message: Message):
    if message.from_id != message.peer_id:
        return
    user_menu_state[message.from_id] = "main"
    await message.answer(
        "Добро пожаловать в ХостингБот! Выбери раздел:",
        keyboard=get_main_menu()
    )

@bot.on.message(attachment="video")
async def video_handler(message: Message):
    if message.from_id != message.peer_id:
        return
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
        keyboard=get_create_links_menu()
    )

@bot.on.message(text=["📸 Создать ссылку", "🎥 Видео", "🖼 Фото (обычная)", "🖼 Фото (Яндекс)", "🎥 Видео (обычная)", "🎥 Видео (Яндекс)", "🌐 Сайт", "ℹ️ Инфо", "👤 Моё", "📝 Отзывы", "💬 Наш чат", "💰 Благотворительность", "🏆 Топ донатеров", "📜 Мои ссылки", "📊 История", "← Назад"])
async def menu_navigation(message: Message):
    if message.from_id != message.peer_id:
        return
    
    user_id = message.from_id
    text = message.text
    
    if text == "📸 Создать ссылку":
        user_menu_state[user_id] = "create"
        await message.answer("Выбери тип ссылки:", keyboard=get_create_links_menu())
    
    elif text == "ℹ️ Инфо":
        user_menu_state[user_id] = "info"
        await message.answer("Информация:", keyboard=get_info_menu())
    
    elif text == "👤 Моё":
        user_menu_state[user_id] = "my"
        await message.answer("Твои данные:", keyboard=get_my_menu())

    elif text == "🖼 Фото (обычная)":
        user_menu_state[user_id] = "waiting_photo"
        await message.answer("Отправь мне фото, и я сделаю из него короткую ссылку!")
    
    elif text == "🖼 Фото (Яндекс)":
        await message.answer(
            "📤 Загрузи фото на Яндекс.Диск по ссылке:\n"
            "https://disk.yandex.ru/client/upload\n"
            "После загрузки отправь мне ссылку — я её сокращу.",
            keyboard=get_create_links_menu()
        )
    
    elif text == "🎥 Видео (обычная)":
        await message.answer("Отправь мне видео, и я сделаю из него короткую ссылку!")
    
    elif text == "🎥 Видео (Яндекс)":
        await message.answer(
            "📤 Загрузи видео на Яндекс.Диск по ссылке:\n"
            "https://disk.yandex.ru/client/upload\n"
            "После загрузки отправь мне ссылку — я её сокращу.",
            keyboard=get_create_links_menu()
        )

    elif text == "🌐 Сайт":
        await message.answer("Отправь ссылку на сайт, и я её сокращу!")
    
    elif text == "📝 Отзывы":
        await message.answer("Оставь отзыв здесь: https://vk.com/wall-236560135_7")
    
    elif text == "💬 Наш чат":
        await message.answer("Присоединяйся к чату: https://vk.me/join/V0Th6yX2jAgaZX1Kmcum2M9togNPA1NCqU=")

    elif text == "💰 Благотворительность":
        await message.answer(
            f"💰 Номер карты Сбера:\n`2202 2081 4442 2046`\n\n"
            f"Спасибо! Если хотите попасть в топ донатеров, отправьте чек перевода и мы добавим вас в список.",
            keyboard=(
                Keyboard(inline=False)
                .add(Text("✅ Я перевёл"), color=KeyboardButtonColor.POSITIVE)
                .row()
                .add(Text("← Назад"), color=KeyboardButtonColor.SECONDARY)
            )
        )
    
    elif text == "✅ Я перевёл":
        await message.answer(
            "📸 Скиньте чек (скриншот перевода), чтобы мы убедились в платеже и добавили вас в список донатеров.",
            keyboard=get_info_menu()
        )

    elif text == "🏆 Топ донатеров":
        current_month = datetime.now().strftime("%Y-%m")
        month_data = []
        for uid, data in donations_db.items():
            if current_month in data.get("months", {}):
                month_data.append((uid, data["months"][current_month]))
        
        if not month_data:
            await message.answer("🏆 Пока нет донатеров в этом месяце.", keyboard=get_info_menu())
            return
        
        month_data.sort(key=lambda x: x[1], reverse=True)
        text = "🏆 **Топ донатеров месяца:**\n\n"
        for i, (uid, amount) in enumerate(month_data[:10], 1):
            try:
                user = await bot.api.users.get(int(uid))
                name = f"{user[0].first_name} {user[0].last_name}"
            except:
                name = f"Пользователь {uid}"
            text += f"{i}. {name} — {amount}₽\n"
        await message.answer(text, keyboard=get_info_menu())

    elif text == "📜 Мои ссылки":
        uid = str(message.from_id)
        if uid not in history_db or not history_db[uid]:
            await message.answer("📜 У тебя пока нет сохранённых ссылок.", keyboard=get_my_menu())
        else:
            lines = ["📜 **Твои последние ссылки:**"]
            for idx, item in enumerate(history_db[uid], 1):
                lines.append(f"{idx}. {item['link']}")
            await message.answer("\n".join(lines), keyboard=get_my_menu())
    
    elif text == "📊 История":
        await message.answer("📊 История (в разработке)", keyboard=get_my_menu())
    
    elif text == "← Назад":
        user_menu_state[user_id] = "main"
        await message.answer("Главное меню:", keyboard=get_main_menu())

@bot.on.message(attachment="photo")
async def photo_handler(message: Message):
    if message.from_id != message.peer_id:
        return
    
    user_id = message.from_id
    if user_menu_state.get(user_id) == "waiting_photo":
        for attachment in message.attachments:
            if attachment.photo:
                photo = attachment.photo
                long_url = photo.sizes[-1].url
                short_url = await shorten_url(long_url)
                photo_id = f"photo{photo.owner_id}_{photo.id}"
                add_link(message.from_id, short_url, "фото")
                await message.answer(
                    f"✅ Готово!\n\n"
                    f"📌 Короткая ссылка:\n{short_url}\n\n"
                    f"📌 Attachment:\n{photo_id}",
                    keyboard=get_create_links_menu()
                )
        user_menu_state[user_id] = "create"
    else:
        await message.answer(
            "📸 Сначала нажми «Фото» в меню «Создать ссылку».",
            keyboard=get_main_menu()
        )

@bot.on.message(text=["чек", "скриншот"])
async def check_handler(message: Message):
    if message.from_id != message.peer_id:
        return
    await message.answer(
        "⏳ Ожидайте... Админ проверит и добавит вас в список донатеров.",
        keyboard=get_info_menu()
    )

@bot.on.message(text=["!топ"])
async def add_donate(message: Message):
    if message.from_id != ADMIN_ID:
        return
    
    parts = message.text.split()
    if len(parts) != 3:
        await message.answer("❌ Формат: !топ [id] [сумма]")
        return
    
    try:
        user_id = parts[1]
        amount = int(parts[2])
    except:
        await message.answer("❌ Ошибка в формате")
        return
    
    month = datetime.now().strftime("%Y-%m")
    
    if user_id not in donations_db:
        donations_db[user_id] = {"total": 0, "months": {}}
    
    if month not in donations_db[user_id]["months"]:
        donations_db[user_id]["months"][month] = 0
    
    donations_db[user_id]["months"][month] += amount
    donations_db[user_id]["total"] += amount
    save_donations(donations_db)
    
    await message.answer(f"✅ Добавлено {amount}₽ пользователю {user_id}")

@bot.on.message()
async def unknown_handler(message: Message):
    if message.from_id != message.peer_id:
        return
    await message.answer(
        "Выбери раздел в меню:",
        keyboard=get_main_menu()
    )

if __name__ == "__main__":
    print("✅ Бот запущен и ждёт сообщения...")
    bot.run_forever()

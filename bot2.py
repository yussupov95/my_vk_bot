from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text
import json
import os
from datetime import datetime

TOKEN = "vk1.a.HEt17KHUp8qmK7p42fTxHpw7vx6Cu4AW5vbPR0m8tWJE_0ha3WPcFGH_HfVGMFHh2G5Ep4VmKZPVqPJ7-r58qY"

bot = Bot(token=TOKEN)

DONATIONS_FILE = "donations.json"
ADMIN_ID = 609908758

def load_donations():
    if os.path.exists(DONATIONS_FILE):
        with open(DONATIONS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_donations(d):
    with open(DONATIONS_FILE, "w") as f:
        json.dump(d, f)

donations_db = load_donations()

@bot.on.message(text=["!топ"])
async def add_donate(message: Message):
    if message.from_id != ADMIN_ID:
        return
    parts = message.text.split()
    if len(parts) != 3:
        await message.answer("❌ Формат: !топ [id] [сумма]")
        return
    try:
        uid = parts[1]
        amount = int(parts[2])
    except:
        await message.answer("❌ Ошибка в формате")
        return
    month = datetime.now().strftime("%Y-%m")
    if uid not in donations_db:
        donations_db[uid] = {"total": 0, "months": {}}
    if month not in donations_db[uid]["months"]:
        donations_db[uid]["months"][month] = 0
    donations_db[uid]["months"][month] += amount
    donations_db[uid]["total"] += amount
    save_donations(donations_db)
    await message.answer(f"✅ Добавлено {amount}₽ пользователю {uid}")

@bot.on.message()
async def handler(message: Message):
    await message.answer("Бот работает. Используй !топ")

if __name__ == "__main__":
    print("✅ Бот запущен")
    bot.run_forever()

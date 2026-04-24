import asyncio
import random
import aiosqlite
from aiogram import Bot, Dispatcher, types
import os

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

bot = Bot(token=TOKEN)
dp = Dispatcher()

POST_LIMIT = 40
INTERVAL = 86400 // POST_LIMIT  # kuniga 40 ta

CAPTIONS = [
    "🔥 Eng zo‘r tanlov!\n",
    "💎 Premium sifat!\n",
    "⚡ Cheklangan dona!\n",
    "👑 Eng ko‘p sotilayotgan!\n"
]

CTA = """
👤 Admin: @shuraparfumes
📞 Telefon: +998 99 228 55 14
📦 Tezkor yetkazib berish

Buyurtma uchun admin bilan bog‘laning ✨
"""

async def init_db():
    async with aiosqlite.connect("db.sqlite") as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id INTEGER
        )
        """)
        await db.commit()

@dp.channel_post()
async def save_post(message: types.Message):
    async with aiosqlite.connect("db.sqlite") as db:
        await db.execute(
            "INSERT INTO posts (message_id) VALUES (?)",
            (message.message_id,)
        )
        await db.commit()

async def get_random_post():
    async with aiosqlite.connect("db.sqlite") as db:
        cursor = await db.execute(
            "SELECT message_id FROM posts ORDER BY RANDOM() LIMIT 1"
        )
        row = await cursor.fetchone()
        return row[0] if row else None

async def repost():
    while True:
        msg_id = await get_random_post()
        if msg_id:
            caption = random.choice(CAPTIONS) + CTA
            await bot.copy_message(
                chat_id=CHANNEL_ID,
                from_chat_id=CHANNEL_ID,
                message_id=msg_id,
                caption=caption
            )
        await asyncio.sleep(INTERVAL)

async def main():
    await init_db()
    asyncio.create_task(repost())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

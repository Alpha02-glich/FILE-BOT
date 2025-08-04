import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, ReplyKeyboardMarkup
from config import API_ID, API_HASH, BOT_TOKEN, PROMO_LINK

import referal_lock  # your referral lock module

app = Client("sexmix_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

STORAGE_CHANNEL = "storgewala"  # Your public channel username (no '@')

def load_video_ids():
    return {
        "indian": [
            {"msg_id": 3, "caption": "🔥 Indian Clip 1"},
            {"msg_id": 4, "caption": "🔥 Indian Clip 2"},
            {"msg_id": 5, "caption": "🔥 Indian Clip 3"},
            {"msg_id": 6, "caption": "🔥 Indian Clip 4"},
            {"msg_id": 7, "caption": "🔥 Indian Clip 5"},
            {"msg_id": 8, "caption": "🔥 Indian Clip 6"},
            {"msg_id": 9, "caption": "🔥 Indian Clip 7"},
        ],
        "russian": [
            {"msg_id": 11, "caption": "💋 Russian Clip 1"},
            {"msg_id": 12, "caption": "💋 Russian Clip 2"},
            {"msg_id": 13, "caption": "💋 Russian Clip 3"},
            {"msg_id": 14, "caption": "💋 Russian Clip 4"},
            {"msg_id": 15, "caption": "💋 Russian Clip 5"},
            {"msg_id": 16, "caption": "💋 Russian Clip 6"},
            {"msg_id": 17, "caption": "💋 Russian Clip 7"},
        ],
        "mms": [
            {"msg_id": 19, "caption": "📸 Viral MMS 1"},
            {"msg_id": 20, "caption": "📸 Viral MMS 2"},
            {"msg_id": 21, "caption": "📸 Viral MMS 3"},
            {"msg_id": 22, "caption": "📸 Viral MMS 4"},
            {"msg_id": 23, "caption": "📸 Viral MMS 5"},
        ]
    }

db = {
    "users": {},
    "categories": load_video_ids()
}

async def auto_delete(message, delay):
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except:
        pass

@app.on_message(filters.command("start"))
async def start_handler(client: Client, message: Message):
    await referal_lock.handle_start(db, client, message)

@app.on_message(filters.text & filters.private)
async def text_category_handler(client, message: Message):
    text = message.text.strip().lower()
    user_id = str(message.from_user.id)

    if text == "📥 indian":
        category = "indian"
    elif text == "📥 russian":
        category = "russian"
    elif text == "📥 viral mms":
        category = "mms"
    else:
        return

    videos = db["categories"].get(category, [])
    if not videos:
        await message.reply(f"No videos found in {category.capitalize()} category!")
        return

    if category == "mms":
        can_access = await referal_lock.check_mms_access(db, client, message)
        if not can_access:
            return

    await message.reply(f"Sending {len(videos)} {category.capitalize()} videos...")

    for video in videos:
        try:
            copied = await client.copy_message(
                chat_id=message.chat.id,
                from_chat_id=STORAGE_CHANNEL,
                message_id=video["msg_id"]
            )
            await copied.edit_caption(video["caption"] + "\n\n" + PROMO_LINK)
            asyncio.create_task(auto_delete(copied, 300))
        except Exception as e:
            await message.reply_text(f"❌ Failed to send video: {e}")

@app.on_callback_query()
async def callback_handler(client, query):
    data = query.data

    if data == "check_joined":
        menu_keyboard = ReplyKeyboardMarkup(
            keyboard=[
                ["📥 INDIAN", "📥 RUSSIAN"],
                ["📥 VIRAL MMS"]
            ],
            resize_keyboard=True,
            one_time_keyboard=False
        )

        try:
            await query.message.delete()
        except:
            pass

        await query.message.reply(
            "✅ Thanks for using our bot.",
            reply_markup=menu_keyboard
        )
        return

    await query.answer("Unknown action.")

app.run()

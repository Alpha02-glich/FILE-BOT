from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def handle_start(db, client, message):
    args = message.text.split()
    user_id = str(message.from_user.id)

    # Referral tracking and notification
    if len(args) > 1:
        referrer_id = args[1]
        if referrer_id != user_id and referrer_id in db["users"]:
            db["users"][referrer_id]["referrals"] = db["users"][referrer_id].get("referrals", 0) + 1

            # Notify referrer about new referral count
            try:
                await client.send_message(
                    chat_id=int(referrer_id),
                    text=f"🎉 You got a new referral! Total referrals: {db[ 'users' ][referrer_id]['referrals']}"
                )
            except Exception as e:
                # In case referrer blocked bot or error occurred, just ignore
                print(f"Failed to notify referrer {referrer_id}: {e}")

    if user_id not in db["users"]:
        db["users"][user_id] = {"referrals": 0}

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 CHANNEL 1", url="https://t.me/+ZrhaQbxi32E5NjBl")],
        [InlineKeyboardButton("📢 CHANNEL 2", url="https://t.me/+CUaO1nkyZ4Y2MTg9")],
        [InlineKeyboardButton("✅ JOINED", callback_data="check_joined")]
    ])

    text = (
        "🔥 VIRAL MMS ONLY HERE\n"
        "👇 START THE BOT AND MAJE LO\n"
        "👾 Made by @MCOGx"
    )

    await message.reply(text, reply_markup=keyboard)

async def check_mms_access(db, client, message):
    user_id = str(message.from_user.id)
    user_data = db["users"].setdefault(user_id, {"referrals": 0})

    if user_data.get("referrals", 0) < 2:
        referral_link = f"https://t.me/{(await client.get_me()).username}?start={user_id}"
        await message.reply(
            f"🔒 You need at least 2 referrals to unlock VIRAL MMS.\n\n"
            f"Your referrals: {user_data.get('referrals', 0)}/2\n"
            f"Share this link with friends:\n{referral_link}\n\n"
            "Once 2 people start the bot via your link, MMS will unlock!"
        )
        return False

    # Deduct 2 referrals after granting access
    db["users"][user_id]["referrals"] -= 2

    await message.reply(
        f"✅ MMS unlocked using 2 referrals.\n"
        f"Remaining referrals: {db['users'][user_id]['referrals']}"
    )

    return True

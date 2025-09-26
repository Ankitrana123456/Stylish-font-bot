import logging, random
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)
from keep_alive import keep_alive  # for 24/7 alive

# ===== CONFIG =====
BOT_TOKEN = "8432126829:AAEujJnVapTFzeuMhEzZfOv9y-boZsx_2uE"
CHANNEL_USERNAME = "@Owner_X_Bots"

logging.basicConfig(level=logging.INFO)
user_favorites = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔗 Join Channel", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")],
        [InlineKeyboardButton("✅ Check Joined", callback_data="check_join")]
    ])
    await update.message.reply_text(
        "👋 Hey!\n\n First Join Our Chanel For Using This Bot And Enjoy 🔥 Then Send Any Text (e.g -`Rana , Ankit`) To get 15+ Stylish Fonts ✨",
        parse_mode="Markdown",
        reply_markup=keyboard
    )

async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
    if member.status in ["member", "administrator", "creator"]:
        await query.edit_message_text("✅ Verified! Now Send Your Text To Get 15+ Stylish Designs 💎")
    else:
        await query.answer("🚫 First Join Our Chanel!", show_alert=True)

def generate_stylish_fonts(text):
    bold = str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳")
    italic = str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", "𝑨𝑩𝑪𝑫𝑬𝑭𝑮𝑯𝑰𝑱𝑲𝑳𝑴𝑵𝑶𝑷𝑸𝑹𝑺𝑻𝑼𝑽𝑾𝑿𝒀𝒁𝒂𝒃𝒄𝒅𝒆𝒇𝒈𝒉𝒊𝒋𝒌𝒍𝒎𝒏𝒐𝒑𝒒𝒓𝒔𝒕𝒖𝒗𝒘𝒙𝒚𝒛")
    cursive = str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", "𝒜𝐵𝒞𝒟𝐸𝐹𝒢𝐻𝐼𝒥𝒦𝐿𝑀𝒩𝒪𝒫𝒬𝑅𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵𝒶𝒷𝒸𝒹𝑒𝒻𝑔𝒽𝒾𝒿𝓀𝓁𝓂𝓃𝑜𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏")

    fancy_fonts = [
        f"★彡 {text.translate(bold)} 彡★",
        f"➤ ☆ {text.translate(bold)}☆❦™",
        f"☞☆ {text.translate(italic)} ❥™",
        f"✿ {text.translate(cursive)} ✿❥™",
        f"𓆩♡𓆪 {text.translate(bold)} 𓆩♡𓆪",
        f"╰☆╮ {text.translate(cursive)} ╰☆╮",
        f"★彡( {text.translate(italic)} )彡★",
        f"🦋 {text.translate(bold)} 🦋",
        f"🌸 {text.translate(cursive)} 🌸",
        f"🔥 {text.translate(bold)} 🔥",
        f"💖 {text.translate(italic)} 💖",
        f"♛ {text.translate(bold)} ♛",
        f"💫『 {text.translate(cursive)} 』💫",
        f"꧁༒☬ {text.translate(bold)} ☬༒꧂",
        f"༺⚡༻ {text.translate(italic)} ༺⚡༻",
    ]
    return fancy_fonts

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.strip()
    fonts = generate_stylish_fonts(user_text)
    context.user_data["fonts"] = fonts
    user_id = update.message.from_user.id
    user_favorites[user_id] = user_favorites.get(user_id, [])

    reply = f"✨ *Stylish Fonts for:* `{user_text}` ✨\n\n"
    for i, f in enumerate(fonts, 1):
        reply += f"{i}. `{f}`\n\n"

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔁 Random Font", callback_data="random_font"),
            InlineKeyboardButton("📋 Copy All", callback_data="copy_all")
        ],
        [
            InlineKeyboardButton("❤️ Save Favorite", callback_data="save_fav"),
            InlineKeyboardButton("🧠 Auto Best", callback_data="auto_best")
        ]
    ])
    await update.message.reply_text(reply, parse_mode="Markdown", reply_markup=keyboard)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    user_id = query.from_user.id
    fonts = context.user_data.get("fonts", [])

    if not fonts:
        await query.answer("❗ First Send Your Text!", show_alert=True)
        return

    if data == "random_font":
        chosen = random.choice(fonts)
        await query.message.reply_text(f"🎲 *Random Font:* \n`{chosen}`", parse_mode="Markdown")

    elif data == "copy_all":
        joined = "\n".join([f"`{f}`" for f in fonts])
        await query.message.reply_text(f"📋 *All Fonts:* \n\n{joined}", parse_mode="Markdown")

    elif data == "save_fav":
        user_favorites[user_id].append(fonts[0])
        await query.answer("❤️ Favorite Saved!")

    elif data == "auto_best":
        best = random.choice(fonts[:5])
        await query.message.reply_text(f"🧠 *AI Picked Best:* \n`{best}`", parse_mode="Markdown")

def main():
    keep_alive()
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_join, pattern="check_join"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("🚀 Bot Running 24/7 on Render...")
    app.run_polling()

if __name__ == "__main__":
    main()

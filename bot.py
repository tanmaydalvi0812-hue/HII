import os

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

FOOTER = "DM FOR INFO\n@KINGxHREE"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Send 3 demo/test lines:\n\n"
        "USERNAME\n"
        "PASSWORD\n"
        "2FA KEY\n\n"
        "Example:\n"
        "demo_user\n"
        "demo_password\n"
        "AAAA BBBB CCCC DDDD"
    )


async def format_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    if len(lines) != 3:
        await update.message.reply_text(
            "❌ Please send exactly 3 lines:\n\n"
            "USERNAME\n"
            "PASSWORD\n"
            "2FA KEY"
        )
        return

    username, password, twofa = lines

    # Demo/test values only.
    if username == "demo_user" and password == "demo_password":
        pass
    else:
        await update.message.reply_text(
            "❌ This demo bot accepts only the example/test values:\n\n"
            "demo_user\n"
            "demo_password\n"
            "AAAA BBBB CCCC DDDD"
        )
        return

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📋 COPY USERNAME",
                callback_data="copy_username"
            )
        ],
        [
            InlineKeyboardButton(
                "📋 COPY PASSWORD",
                callback_data="copy_password"
            )
        ],
        [
            InlineKeyboardButton(
                "📋 COPY 2FA KEY",
                callback_data="copy_2fa"
            )
        ],
    ])

    result = (
        f"USERNAME: {username}\n"
        f"PASSWORD: {password}\n"
        f"2FA KEY: {twofa}\n\n"
        f"{FOOTER}"
    )

    await update.message.reply_text(
        result,
        reply_markup=keyboard
    )


async def copy_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    values = {
        "copy_username": "demo_user",
        "copy_password": "demo_password",
        "copy_2fa": "AAAA BBBB CCCC DDDD",
    }

    value = values.get(query.data)

    if value:
        # Telegram bots cannot directly write to a user's clipboard.
        # Instead, send the value so the user can copy it normally.
        await query.message.reply_text(f"`{value}`", parse_mode="Markdown")


def main():
    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN environment variable is not set."
        )

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            format_message
        )
    )

    app.add_handler(
        CallbackQueryHandler(copy_button)
    )

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()

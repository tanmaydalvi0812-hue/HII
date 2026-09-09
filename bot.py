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
        "Send 3 lines of non-sensitive demo data:\n\n"
        "LINE 1\n"
        "LINE 2\n"
        "LINE 3"
    )


async def format_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    lines = text.splitlines()

    if len(lines) != 3:
        await update.message.reply_text(
            "❌ Please send exactly 3 lines."
        )
        return

    line1 = lines[0].strip()
    line2 = lines[1].strip()

    # Preserve line 3 exactly as entered, including spaces.
    line3 = lines[2].strip()

    result = (
        f"LINE 1: {line1}\n"
        f"LINE 2: {line2}\n"
        f"LINE 3: {line3}\n\n"
        f"{FOOTER}"
    )

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📋 COPY LINE 1",
                callback_data="copy_1"
            )
        ],
        [
            InlineKeyboardButton(
                "📋 COPY LINE 2",
                callback_data="copy_2"
            )
        ],
        [
            InlineKeyboardButton(
                "📋 COPY LINE 3",
                callback_data="copy_3"
            )
        ],
    ])

    # Store only temporarily for this chat interaction.
    context.user_data["formatted_values"] = [
        line1,
        line2,
        line3,
    ]

    await update.message.reply_text(
        result,
        reply_markup=keyboard
    )


async def copy_value(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    values = context.user_data.get("formatted_values", [])

    mapping = {
        "copy_1": 0,
        "copy_2": 1,
        "copy_3": 2,
    }

    index = mapping.get(query.data)

    if index is None or index >= len(values):
        await query.message.reply_text("❌ Data expired.")
        return

    value = values[index]

    await query.message.reply_text(
        f"`{value}`",
        parse_mode="MarkdownV2"
    )


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
        CallbackQueryHandler(copy_value)
    )

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()

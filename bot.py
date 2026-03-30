import os
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from google import genai

# 🔐 Tokens from Render ENV
BOT_TOKEN = os.getenv("BOT_TOKEN")

API_KEYS = [
    os.getenv("GEMINI_API_KEY1"),
    os.getenv("GEMINI_API_KEY2"),
    os.getenv("GEMINI_API_KEY3"),
]

# 🚀 Message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    if not user_message:
        return

    try:
        # Random API key select
        api_key = random.choice(API_KEYS)

        # Gemini client
        client = genai.Client(api_key=api_key)

        # AI response
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_message
        )

        reply = response.text if response.text else "Koi reply nahi aaya 😅"

    except Exception as e:
        print("Error:", e)
        reply = "Bhai thoda error aa gaya 😅 try again"

    await update.message.reply_text(reply)


# 🔥 Main start
if __name__ == "__main__":
    print("Bot starting... 🚀")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("Bot running ✅")
    app.run_polling()

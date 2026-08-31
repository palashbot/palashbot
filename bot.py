import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")

# Render-এর জন্য ছোট web server
web = Flask(__name__)

@web.route("/")
def home():
    return "Palash Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    web.run(host="0.0.0.0", port=port)

# Telegram /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("হ্যালো! 👋 আমি Palash Bot।")

# যেকোনো message-এর উত্তর
 async def reply(update: update, context: ContextTypes.DEFAULT_TYPE):
text = update.message.text.lower () if "hello or "hi in text: await update.message.reply_text ("👋 হ্যালো! কেমন আছো?") elif "কেমন আছো" in text : await update.message.reply_text ("😊 আমি ভালো আছি। তুমি কেমন আছো?") elif "তোমার নাম" in text: await update.message.reply_text("হ্যালো ("🤖 আমার নাম Palash AI Bot।") elif "ধন্যবাদ" in text: await update.message.reply_text("হ্যালো  ("❤️ স্বাগতম!") elif ("গুডবাই", "goodbye") in text : await update.message.reply_text ("👋 ভালো থেকো। আবার কথা হবে।") else : await update.message.reply_text (f"তুমি লিখেছ: {text}") এখন def main()
    if not TOKEN:
        print("BOT_TOKEN পাওয়া যায়নি!")
        return

    # Web server চালু
    threading.Thread(target=run_web, daemon=True).start()

    # Telegram bot চালু
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

    print("Palash Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()

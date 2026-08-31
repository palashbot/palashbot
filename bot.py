import os
import threading

from flask import Flask
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")


# =========================
# Web Server
# =========================

app = Flask(__name__)


@app.route("/")
def home():
    return "Palash Bot is running!"


def run_web():
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


# =========================
# /start command
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "হ্যালো! 👋 আমি Palash AI Bot।\n\n"
        "আমাকে যেকোনো প্রশ্ন করতে পারো। 🤖"
    )


# =========================
# Questions & Answers
# =========================

ANSWERS = {

    # Greeting
    "হ্যালো": "👋 হ্যালো! কেমন আছো?",
    "হাই": "👋 হাই! 😊",
    "hello": "👋 Hello! কেমন আছো?",
    "hi": "👋 হাই! 😊",
    "হেই": "😄 হেই! কেমন আছো?",
    "সালাম": "ওয়ালাইকুমুস সালাম! ❤️",
    "আসসালামু আলাইকুম": "ওয়ালাইকুমুস সালাম! 😊",

    # About bot
    "তুমি কে": "🤖 আমি Palash AI Bot। তোমার সাথে কথা বলার জন্য তৈরি।",
    "কে তুমি": "🤖 আমি Palash AI Bot।",
    "তোমার নাম": "🤖 আমার নাম Palash AI Bot।",
    "তোমার নাম কি": "🤖 আমার নাম Palash AI Bot।",
    "তোমার নাম কী": "🤖 আমার নাম Palash AI Bot।",
    "তুমি কি রোবট": "🤖 হ্যাঁ, আমি একটি AI Telegram Bot।",
    "তুমি কি মানুষ": "🤖 না, আমি মানুষ নই। আমি একটি AI Bot।",
    "তোমাকে কে বানিয়েছে": "🤖 আমাকে Palash তৈরি করেছে। ❤️",
    "তোমাকে কে বানায়": "🤖 আমাকে Palash তৈরি করেছে। 😎",
    "কে তোমাকে বানিয়েছে": "🤖 আমাকে Palash তৈরি করেছে।",
    "তুমি কোথায় থাকো": "☁️ আমি অনলাইনে সার্ভারে চলি।",

    # Feelings
    "কেমন আছো": "😊 আমি ভালো আছি। তুমি কেমন আছো?",
    "কেমন আছেন": "😊 আমি ভালো আছি। আপনি কেমন আছেন?",
    "ভালো আছো": "😄 হ্যাঁ, আমি ভালো আছি!",
    "তুমি কি খুশি": "😄 তোমার সাথে কথা বলতে আমার ভালো লাগে!",
    "তুমি কি ঘুমাও": "😂 না, আমার ঘুমানোর দরকার হয় না!",
    "তুমি কি খাও": "😂 না, আমি খাবার খাই না!",
    "তুমি কি ক্লান্ত": "🤖 না, আমি ক্লান্ত হই না।",

    # Thanks
    "ধন্যবাদ": "❤️ স্বাগতম!",
    "অনেক ধন্যবাদ": "🥰 তোমাকেও অনেক ধন্যবাদ!",
    "থ্যাংকস": "😊 Welcome!",
    "thanks": "❤️ You're welcome!",
    "thank you": "❤️ You're welcome!",

    # Goodbye
    "বিদায়": "👋 ভালো থেকো। আবার কথা হবে!",
    "গুডবাই": "👋 ভালো থেকো। আবার কথা হবে!",
    "goodbye": "👋 Bye! আবার কথা হবে।",
    "বাই": "👋 বাই! ভালো থেকো।",

    # Friendship
    "তুমি কি আমার বন্ধু": "🥰 অবশ্যই! আমি তোমার AI বন্ধু।",
    "তুমি আমার বন্ধু": "❤️ হ্যাঁ, অবশ্যই!",
    "আমি তোমাকে ভালোবাসি": "❤️ তোমার ভালোবাসার জন্য ধন্যবাদ!",
    "তুমি ভালো": "🥰 ধন্যবাদ!",
    "তুমি পাগল": "🤣 একটু AI-পাগলামি আছে!",
    "তুমি বুদ্ধিমান": "😎 ধন্যবাদ! আমি আমার সাধ্যমতো সাহায্য করি।",

    # Fun
    "একটা জোক বলো": "😂 শিক্ষক: সবচেয়ে অলস কে?\nছাত্র: যে উত্তর দিতে চায় না!",
    "জোক বল": "🤣 কম্পিউটার ডাক্তারকে বলল—আমার ভাইরাস হয়েছে!",
    "গান গাও": "🎵 আমি গান গাইতে পারি না, তবে গান নিয়ে কথা বলতে পারি! 😄",
    "তুমি হাসতে পারো": "😂 হাহাহা! অবশ্যই!",
    "মজা কর": "🤣 জীবন ছোট, তাই একটু মজা করতেই হয়!",

    # Bangladesh
    "বাংলাদেশের রাজধানী কি": "🇧🇩 বাংলাদেশের রাজধানী ঢাকা।",
    "বাংলাদেশের রাজধানী কী": "🇧🇩 বাংলাদেশের রাজধানী ঢাকা।",
    "বাংলাদেশের মুদ্রার নাম কি": "🇧🇩 বাংলাদেশের মুদ্রার নাম টাকা।",
    "বাংলাদেশের ভাষা কি": "🇧🇩 বাংলাদেশের রাষ্ট্রভাষা বাংলা।",
    "বাংলাদেশের জাতীয় ফুল কি": "🌸 বাংলাদেশের জাতীয় ফুল শাপলা।",
    "বাংলাদেশের জাতীয় পাখি কি": "🐦 বাংলাদেশের জাতীয় পাখি দোয়েল।",
    "বাংলাদেশের জাতীয় পশু কি": "🐅 বাংলাদেশের জাতীয় পশু রয়েল বেঙ্গল টাইগার।",
    "বাংলাদেশের জাতীয় ফল কি": "🍈 বাংলাদেশের জাতীয় ফল কাঁঠাল।",
    "বাংলাদেশের জাতীয় মাছ কি": "🐟 বাংলাদেশের জাতীয় মাছ ইলিশ।",
    "বাংলাদেশের জাতীয় খেলা কি": "🏏 বাংলাদেশের জাতীয় খেলা কাবাডি।",

    # Programming
    "python কি": "🐍 Python একটি জনপ্রিয় programming language।",
    "পাইথন কি": "🐍 Python একটি জনপ্রিয় programming language।",
    "html কি": "🌐 HTML ওয়েব পেজের structure তৈরি করতে ব্যবহৃত হয়।",
    "css কি": "🎨 CSS ওয়েবসাইটের design ও style করার জন্য ব্যবহৃত হয়।",
    "javascript কি": "⚡ JavaScript ওয়েবসাইটকে interactive করতে ব্যবহৃত হয়।",
    "api কি": "🔌 API-এর মাধ্যমে বিভিন্ন software একে অপরের সাথে যোগাযোগ করতে পারে।",
    "bot কি": "🤖 Bot হলো এমন software যা নির্দিষ্ট কাজ স্বয়ংক্রিয়ভাবে করতে পারে।",
    "telegram bot কি": "🤖 Telegram Bot হলো Telegram-এর মধ্যে স্বয়ংক্রিয়ভাবে কাজ করা program।",
    "server কি": "🖥️ Server হলো এমন system যা অন্যদের জন্য service বা data সরবরাহ করে।",
    "deploy কি": "🚀 Deploy মানে application-কে server-এ চালু করা।",
    "render কি": "🚀 Render হলো cloud platform যেখানে application deploy করা যায়।",

    # সাধারণ প্রশ্ন
    "কি খবর": "😄 ভালো খবর! তোমার খবর কী?",
    "কী খবর": "😄 সব ভালো! তোমার খবর কী?",
    "কি করো": "🤖 তোমার প্রশ্নের উত্তর দেওয়ার চেষ্টা করি।",
    "কী করো": "🤖 তোমার সাথে কথা বলি এবং সাহায্য করার চেষ্টা করি।",
    "তুমি কি অনলাইনে": "🌐 হ্যাঁ, আমি অনলাইনে আছি।",
    "সাহায্য করো": "🤝 অবশ্যই! কী নিয়ে সাহায্য দরকার বলো।",
    "আমাকে সাহায্য কর": "🤝 অবশ্যই! কী সমস্যা হয়েছে বলো।",
    "শুভ সকাল": "🌅 শুভ সকাল! তোমার দিনটি সুন্দর হোক।",
    "শুভ রাত্রি": "🌙 শুভ রাত্রি! ভালো ঘুম হোক।",
    "শুভ সন্ধ্যা": "🌆 শুভ সন্ধ্যা! কেমন কাটছে দিন?",
}


# =========================
# Message Reply
# =========================

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):

    original_text = update.message.text
    text = original_text.lower().strip()

    # প্রথমে সরাসরি প্রশ্ন খুঁজবে
    if text in ANSWERS:
        await update.message.reply_text(ANSWERS[text])
        return

    # এরপর বাক্যের মধ্যে keyword খুঁজবে
    if "তোমার নাম" in text:
        await update.message.reply_text(
            "🤖 আমার নাম Palash AI Bot।"
        )
        return

    if "কে বানিয়েছে" in text or "কে বানায়" in text:
        await update.message.reply_text(
            "🤖 আমাকে Palash তৈরি করেছে। ❤️"
        )
        return

    if "কেমন আছ" in text:
        await update.message.reply_text(
            "😊 আমি ভালো আছি। তুমি কেমন আছো?"
        )
        return

    if "ধন্যবাদ" in text or "thanks" in text:
        await update.message.reply_text(
            "❤️ স্বাগতম!"
        )
        return

    if "গুডবাই" in text or "goodbye" in text:
        await update.message.reply_text(
            "👋 ভালো থেকো। আবার কথা হবে!"
        )
        return

    # প্রশ্ন database-এ না থাকলে
    await update.message.reply_text(
        "🤔 এই প্রশ্নের উত্তর এখনো আমার জানা নেই।\n\n"
        f"তুমি লিখেছ: {original_text}"
    )


# =========================
# Main
# =========================

def main():

    if not TOKEN:
        print("BOT_TOKEN পাওয়া যায়নি!")
        return

    # Web server চালু
    threading.Thread(
        target=run_web,
        daemon=True
    ).start()

    # Telegram bot চালু
    application = (
        Application
        .builder()
        .token(TOKEN)
        .build()
    )

    # /start
    application.add_handler(
        CommandHandler("start", start)
    )

    # সাধারণ message
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            reply
        )
    )

    print("Palash AI Bot is running...")

    application.run_polling()


if __name__ == "__main__":
    main()

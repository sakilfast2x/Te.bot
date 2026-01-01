import logging
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
import google.generativeai as genai

# =========================
# 🌐 WEB SERVER FOR RENDER (Keep Alive)
# =========================
server = Flask('')

@server.route('/')
def home():
    return "Bot is running!"

def run_server():
    server.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_server)
    t.start()

# =========================
# 🔑 CONFIG
# =========================
BOT_TOKEN = "7980795853:AAFHcODyJ73c2vxrlhULb7x_UP_q89f-SgQ"
GEMINI_API_KEY = "AIzaSyBVhUlGH5InQ-8rtzpizy2_Zm-Vg1UCIyY"

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="You are a smart Telegram AI assistant. Bangla input -> Bangla reply, English input -> English reply"
)

logging.basicConfig(level=logging.INFO)

# =========================
# 🚀 HANDLERS
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✨✨✨ 2X FAST TEAM ✨✨✨\n"
        "🔥 Created by SAKIL 🔥\n\n"
        "🤖 Welcome to SAKIL AI\n"
        "💬 Ask your question"
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.text: return
    try:
        response = model.generate_content(update.message.text)
        reply = response.text
    except Exception:
        reply = "⚠️ Server busy, please try again later."
    await update.message.reply_text(reply)

# =========================
# 🧠 MAIN
# =========================
def main():
    # Render-এর জন্য ওয়েব সার্ভার চালু করা
    keep_alive()
    
    # নতুন ভার্সনের সঠিক ফরম্যাট
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("🤖 Bot Started...")
    app.run_polling()

if __name__ == "__main__":
    main()
  

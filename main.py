import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

genai.configure(
    api_key=os.getenv('GEMINI_API_KEY'),
    client_options={'api_endpoint': 'https://generativelanguage.googleapis.com'}
)
model = genai.GenerativeModel('gemini-pro')

async def reply_with_gemini(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_username = "@shadow72ru_bot"
    if bot_username in update.message.text:
        user_question = update.message.text.replace(bot_username, "").strip()
        try:
            response = model.generate_content(user_question)
            await update.message.reply_text(response.text)
        except Exception as e:
            # Бот пришлет ошибку прямо в чат!
            error_text = f"Ошибка: {str(e)}"
            await update.message.reply_text(error_text)

if __name__ == '__main__':
    token = os.getenv('TELEGRAM_TOKEN')
    app = ApplicationBuilder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT & filters.Entity("mention"), reply_with_gemini))
    print("Бот запущен...")
    app.run_polling()

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
    # Теперь ищем имя бота просто как текст, без сложных фильтров
    if "@shadow72ru_bot" in update.message.text:
        user_question = update.message.text.replace("@shadow72ru_bot", "").strip()
        try:
            response = model.generate_content(user_question)
            await update.message.reply_text(response.text)
        except Exception as e:
            await update.message.reply_text(f"Ошибка: {str(e)}")

if __name__ == '__main__':
    token = os.getenv('TELEGRAM_TOKEN')
    app = ApplicationBuilder().token(token).build()
    
    # Реакция на любой текст
    app.add_handler(MessageHandler(filters.TEXT, reply_with_gemini))
    
    print("Бот запущен и ждет сообщений...")
    app.run_polling()

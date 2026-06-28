import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Настройка Gemini
# Используем стандартный эндпоинт, но добавили обработку ошибок для диагностики
genai.configure(
    api_key=os.getenv('GEMINI_API_KEY'),
    client_options={'api_endpoint': 'https://generativelanguage.googleapis.com'}
)
model = genai.GenerativeModel('gemini-pro')

async def reply_with_gemini(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_username = "@shadow72ru_bot"
    if bot_username in update.message.text:
        # Убираем имя бота из запроса
        user_question = update.message.text.replace(bot_username, "").strip()
        
        # Получаем ответ от Gemini с детальным выводом ошибки
        try:
            response = model.generate_content(user_question)
            await update.message.reply_text(response.text)
        except Exception as e:
            # Теперь бот напишет в чат реальную причину ошибки
            error_message = f"Ошибка: {str(e)}"
            print(error_message)
            await update.message.reply_text(f"Не удалось получить ответ от ИИ. {error_message}")

if __name__ == '__main__':
    token = os.getenv('TELEGRAM_TOKEN')
    app = ApplicationBuilder().token(token).build()

    # Бот реагирует только на текст с упоминанием
    app.add_handler(MessageHandler(filters.TEXT & filters.Entity("mention"), reply_with_gemini))

    print("Бот с интеллектом Gemini запущен...")
    app.run_polling()

import os
import g4f
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Бот реагирует только если его упомянули
    if "@shadow72ru_bot" in update.message.text:
        user_text = update.message.text.replace("@shadow72ru_bot", "").strip()
        try:
            # Используем g4f для получения ответа без API ключей
            response = g4f.ChatCompletion.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": user_text}]
            )
            await update.message.reply_text(response)
        except Exception as e:
            await update.message.reply_text("Ошибка при генерации ответа.")

if __name__ == '__main__':
    # Токен берется из переменных окружения
    app = Application.builder().token(os.getenv('TELEGRAM_TOKEN')).build()
    
    # Добавляем обработчик текста
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Бот запущен!")
    # drop_pending_updates=True принудительно убивает старые "зависшие" запросы
    app.run_polling(drop_pending_updates=True)

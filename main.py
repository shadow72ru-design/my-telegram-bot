import os
import g4f
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from collections import defaultdict

# Словарь для хранения истории сообщений (в оперативной памяти)
user_histories = defaultdict(list)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "@shadow72ru_bot" in update.message.text:
        user_id = update.message.from_user.id
        user_text = update.message.text.replace("@shadow72ru_bot", "").strip()
        
        # Добавляем сообщение пользователя в историю
        user_histories[user_id].append({"role": "user", "content": user_text})
        
        # Ограничиваем размер памяти (последние 10 сообщений), чтобы не перегрузить бота
        if len(user_histories[user_id]) > 30:
            user_histories[user_id].pop(0)

        try:
            # Отправляем всю накопленную историю в модель
            response = g4f.ChatCompletion.create(
                model="gpt-4o",
                messages=user_histories[user_id]
            )
            
            # Сохраняем ответ модели в историю
            user_histories[user_id].append({"role": "assistant", "content": response})
            
            await update.message.reply_text(response)
        except Exception as e:
            await update.message.reply_text("Ошибка памяти.")

if __name__ == '__main__':
    app = Application.builder().token(os.getenv('TELEGRAM_TOKEN')).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling(drop_pending_updates=True)

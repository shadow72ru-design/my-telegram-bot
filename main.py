import os
import g4f
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from collections import defaultdict

# Словарь для хранения истории сообщений
user_histories = defaultdict(list)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Условие: упоминание бота ИЛИ ответ на его сообщение
    is_mention = "@shadow72ru_bot" in (update.message.text or "")
    is_reply = update.message.reply_to_message and update.message.reply_to_message.from_user.is_bot
    
    if is_mention or is_reply:
        user_id = update.message.from_user.id
        user_text = (update.message.text or "").replace("@shadow72ru_bot", "").strip()
        
        if not user_text:
            return

        user_histories[user_id].append({"role": "user", "content": user_text})
        
        # Лимит истории 30 сообщений
        if len(user_histories[user_id]) > 30:
            user_histories[user_id].pop(0)

        try:
            response = g4f.ChatCompletion.create(
                model="gpt-4o",
                messages=user_histories[user_id]
            )
            
            user_histories[user_id].append({"role": "assistant", "content": response})
            await update.message.reply_text(response)
        except Exception:
            await update.message.reply_text("Ошибка памяти.")

if __name__ == '__main__':
    app = Application.builder().token(os.getenv('TELEGRAM_TOKEN')).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling(drop_pending_updates=True)

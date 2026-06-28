import os
import g4f
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from collections import defaultdict

# Словарь для хранения истории сообщений
user_histories = defaultdict(list)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Преобразуем текст в нижний регистр для удобства проверки
    text = (update.message.text or "").lower()
    
    # Проверка условий активации:
    # 1. Начинается с "бот "
    # 2. Содержит старый ник @shadow72ru_bot
    # 3. Является ответом на сообщение бота (реплай)
    is_mention = text.startswith("бот ") or "@shadow72ru_bot" in text
    is_reply = update.message.reply_to_message and update.message.reply_to_message.from_user.is_bot
    
    if is_mention or is_reply:
        user_id = update.message.from_user.id
        
        # Очищаем текст от ключевых слов "Бот " или ника для передачи в нейросеть
        user_text = update.message.text.replace("@shadow72ru_bot", "").replace("бот ", "", 1).replace("Бот ", "", 1).strip()
        
        if not user_text:
            return

        # Системная инструкция для краткости и запрета ссылок
        if not any(msg.get("role") == "system" for msg in user_histories[user_id]):
            user_histories[user_id].insert(0, {"role": "system", "content": "Ты — краткий помощник. Отвечай по делу. Если используешь поиск, не присылай ссылки, сноски и технический текст. Пиши только чистый, понятный ответ."})
            
        # Добавляем сообщение пользователя в историю
        user_histories[user_id].append({"role": "user", "content": user_text})
        
        # Лимит истории (30 сообщений + 1 системное)
        if len(user_histories[user_id]) > 31: 
            user_histories[user_id].pop(1) 

        try:
            # Генерация ответа через модель
            response = g4f.ChatCompletion.create(
                model="gpt-4o",
                messages=user_histories[user_id]
            )
            
            # Сохраняем ответ в историю
            user_histories[user_id].append({"role": "assistant", "content": response})
            await update.message.reply_text(response)
        except Exception:
            await update.message.reply_text("Ошибка при обработке запроса.")

if __name__ == '__main__':
    # Запуск бота с токеном из переменных окружения
    app = Application.builder().token(os.getenv('TELEGRAM_TOKEN')).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling(drop_pending_updates=True)

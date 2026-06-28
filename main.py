import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Функция, которая проверяет упоминание и отвечает
async def reply_on_mention(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Проверяем, есть ли упоминание бота в сообщении
    bot_username = "@shadow72ru_bot"
    if bot_username in update.message.text:
        await update.message.reply_text(f'Вы обратились ко мне: {update.message.text.replace(bot_username, "").strip()}')

if __name__ == '__main__':
    token = os.getenv('TELEGRAM_TOKEN')
    app = ApplicationBuilder().token(token).build()

    # Фильтруем сообщения: только те, что содержат текст и упоминание
    app.add_handler(MessageHandler(filters.TEXT & filters.Entity("mention"), reply_on_mention))

    print("Бот настроен на реакцию только по имени...")
    app.run_polling()

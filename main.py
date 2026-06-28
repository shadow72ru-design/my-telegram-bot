import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Функция для команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Бот запущен и готов к работе!')

# Функция для ответов на любые текстовые сообщения
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'Вы написали: {update.message.text}')

if __name__ == '__main__':
    token = os.getenv('TELEGRAM_TOKEN')
    app = ApplicationBuilder().token(token).build()

    # Добавляем обработчики
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))

    print("Бот работает...")
    app.run_polling()

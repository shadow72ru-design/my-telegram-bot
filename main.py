import os
from telegram.ext import ApplicationBuilder

async def start(update, context):
    await update.message.reply_text('Бот запущен!')

if __name__ == '__main__':
    TOKEN = os.getenv('TELEGRAM_TOKEN')
    app = ApplicationBuilder().token(TOKEN).build()
    print("Бот работает...")
    app.run_polling()
  

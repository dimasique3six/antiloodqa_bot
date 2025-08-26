from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TOKEN = "ВАШ ТОКЕН"

async def debug_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("chat_id:", update.effective_chat.id)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, debug_chat_id))
    app.run_polling()

if __name__ == "__main__":
    main()
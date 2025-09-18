import re
import unicodedata
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Токен бота
TOKEN = "ТУТ ВСТАВЛЯЕМ ТОКЕН БОТА"
# chat_id группы
CHAT_ID = -100... # ТУТ ВСТАВЛЯЕМ ЧАТ АЙДИ, КОТОРЫЙ ПОЛУЧИЛИ С ПОМОЩЬЮ get_chat_id.py

# Игровые эмодзи (оба варианта, с и без U+FE0F)
GAME_EMOJIS = {
    "🎰",      # слот-машина
    "⚽️", "⚽️", # футбол
    "🏀", "🏀️", # баскетбол
    "🎳",      # боулинг
    "🎯",      # дартс
    "🎲"       # кубик
}

# Регулярка для удаления variation selector (U+FE0F)
variation_selector_pattern = re.compile(r"\uFE0F")


def normalize_text(text: str) -> str:
    """Удаляем variation selectors и нормализуем Unicode"""
    text = variation_selector_pattern.sub("", text)
    return unicodedata.normalize("NFKC", text)


async def delete_spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Удаляет игровые эмодзи из текста и dice-сообщений"""
    msg = update.message
    if not msg:
        return

    # Dice-анимация
    if msg.dice:
        emoji = normalize_text(msg.dice.emoji)
        if emoji in {normalize_text(e) for e in GAME_EMOJIS}:
            await msg.delete()
        return

    # Текстовые сообщения
    if msg.text:
        text = msg.text.strip()
        norm_text = normalize_text(text)
        if all(normalize_text(ch) in {normalize_text(e) for e in GAME_EMOJIS} for ch in text) and text.replace(" ", "") != "":
            await msg.delete()


async def on_startup(app: Application):
    """Сообщение при запуске бота"""
    await app.bot.send_message(CHAT_ID, "АНТИЛУДКА_БОТ2000 ЗАПУЩЕН.")


def main():
    app = Application.builder().token(TOKEN).post_init(on_startup).build()
    app.add_handler(MessageHandler(filters.ALL, delete_spam))
    print("Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()

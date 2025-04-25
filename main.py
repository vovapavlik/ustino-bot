from flask import Flask, request
import telegram
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

# Временное хранилище корзины
user_carts = {}

@app.route("/")
def index():
    return "Ustino Bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    text = update.message.text.lower()

    if text == "/start":
        bot.send_message(chat_id=chat_id, text="Добро пожаловать в Ustino!", reply_markup=start_keyboard())
    elif text == "🛍 каталог":
        bot.send_message(chat_id=chat_id, text="Каталог пока в разработке.")
    elif text == "🛒 корзина":
        cart = user_carts.get(chat_id, [])
        message = "Ваша корзина:
" + "\n".join(cart) if cart else "Ваша корзина пуста."
        bot.send_message(chat_id=chat_id, text=message)
    elif text == "✅ оформить заказ":
        bot.send_message(chat_id=chat_id, text="Пожалуйста, отправьте ФИО, адрес и номер телефона в одном сообщении.")
    elif text.startswith("фио") or text.startswith("адрес") or text.startswith("телефон"):
        tg_link = f"https://t.me/ustino_fashion"
        bot.send_message(chat_id=chat_id, text=f"Спасибо за заказ! Наш менеджер свяжется с вами. Напишите нам: {tg_link}")
    elif text == "⭐ отзывы":
        bot.send_message(chat_id=chat_id, text="Отзывы можно посмотреть в нашей группе VK.")
    elif text == "📍 где мы находимся":
        bot.send_message(chat_id=chat_id, text="Смотри наш адрес и контакты здесь: https://vk.me/ustino_fashion")
    else:
        bot.send_message(chat_id=chat_id, text="Выберите команду из меню.")

    return "ok"

def start_keyboard():
    keyboard = telegram.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("🛍 Каталог", "🛒 Корзина")
    keyboard.add("✅ Оформить заказ", "⭐ Отзывы")
    keyboard.add("📍 Где мы находимся")
    return keyboard

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

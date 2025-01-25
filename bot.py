import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import re

# Markdown belgilarini qochirish funksiyasi
def escape_markdown(text, version=2):
    """Markdown belgilarini qochirish uchun funksiya."""
    escape_chars = r'\*_`\[]()~>#+-=|{}.!'
    if version == 1:
        escape_chars = r'\*_`\['
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

# Botning tokeni
TOKEN = '7889704052:AAERGo2fRb_Fhdohkb1tB4cFyJ_Mqw5odSI'
bot = telebot.TeleBot(TOKEN)

# Admin username
ADMIN_USERNAME = "@USD_077"

# UC paketlari va narxlari
uc_packages = {
    '🎮 30 + 2 UC': 7200,
    '🎮 60 + 3 UC': 12500,
    '🎮 300 + 40 UC': 61000,
    '🎮 600 + 90 UC': 118500,
    '🎮 1500 + 375 UC': 295000,
    '🎮 3000 + 1000 UC': 582000,
    '🎮 6000 + 2400 UC': 1130000,
    '🎮 12000 + 4800 UC': 2370000,
    '🎮 18000 + 7200 UC': 3530000,
    '🎮 24000 + 9600 UC': 4720000,
    '🎮 30000 + 12000 UC': 5883000,
    '🎮 60000 + 24000 UC': 11705000,
}

# Telegram Stars narxlari
telegram_stars = {
    '⭐ 100 Stars': 27000,
    '⭐ 150 Stars': 38999,
    '⭐ 250 Stars': 62999,
    '⭐ 350 Stars': 85999,
    '⭐ 500 Stars': 119999,
    '⭐ 750 Stars': 177999,
    '⭐ 1,000 Stars': 235999,
    '⭐ 1,500 Stars': 352999,
    '⭐ 2,500 Stars': 582999,
    '⭐ 5,000 Stars': 1162999,
    '⭐ 10,000 Stars': 2302999,
    '⭐ 25,000 Stars': 5803999,
    '⭐ 50,000 Stars': 11603999,
    '⭐ 100,000 Stars': 23004999,
    '⭐ 150,000 Stars': 35004999,
}

# Telegram Premium paketlari va narxlari
telegram_premium = {
    '✨ 1 oylik Premium': 45000,
    '✨ 1 yillik Premium': 285000,
    '🎁 3 oylik Premium (sovg\'a)': 165000,
    '🎁 6 oylik Premium (sovg\'a)': 215000,
    '🎁 1 yillik Premium (sovg\'a)': 380000,
}

# Bosh menyu inline klaviaturasi
def main_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton('⭐ Telegram Stars', callback_data='stars'),
               InlineKeyboardButton('🎮 UC Service', callback_data='uc_service'),
               InlineKeyboardButton('✨ Telegram Premium', callback_data='premium_service'))
    return markup

# Bosh menyuga o'tish inline klaviaturasi
def back_to_main_menu():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton('🔙 Bosh menyuga oʻtish', callback_data='back_to_main'))
    return markup

# Start komandasi
@bot.message_handler(commands=['start'])
def welcome(message):
    username = message.from_user.username or "foydalanuvchi"
    sent_message = bot.send_message(
        message.chat.id,
        escape_markdown(
            f"👋 Assalomu alaykum, @{username}!\n\n"
            "📋 Quyidagi xizmatlardan birini tanlang:\n\n"
            "⭐ Telegram Stars.\n"
            "🎮 UC Service.\n"
            "✨ Telegram Premium."
        ),
        reply_markup=main_menu(),
        parse_mode='MarkdownV2'
    )

# Telegram Stars tugmasi uchun javob
@bot.callback_query_handler(func=lambda call: call.data == 'stars')
def select_telegram_stars(call):
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=escape_markdown("⭐ Telegram Stars paketlaridan birini tanlang:"),
        reply_markup=generate_markup(telegram_stars, 'stars'),
        parse_mode='MarkdownV2'
    )

# UC Service tugmasi uchun javob
@bot.callback_query_handler(func=lambda call: call.data == 'uc_service')
def select_uc_service(call):
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=escape_markdown("🎮 UC paketlaridan birini tanlang:"),
        reply_markup=generate_markup(uc_packages, 'uc'),
        parse_mode='MarkdownV2'
    )

# Telegram Premium tugmasi uchun javob
@bot.callback_query_handler(func=lambda call: call.data == 'premium_service')
def select_premium_service(call):
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=escape_markdown("✨ Telegram Premium paketlaridan birini tanlang:"),
        reply_markup=generate_markup(telegram_premium, 'premium'),
        parse_mode='MarkdownV2'
    )

# Paketlarni tanlash funksiyasi
def generate_markup(packages, callback_prefix):
    markup = InlineKeyboardMarkup(row_width=2)
    for pkg, price in packages.items():
        markup.add(InlineKeyboardButton(f"{pkg} - {price:,} so'm", callback_data=f"{callback_prefix}_{pkg}"))
    markup.add(InlineKeyboardButton('🔙 Bosh menyuga oʻtish', callback_data='back_to_main'))
    return markup

# Telegram Stars paketini tanlash
@bot.callback_query_handler(func=lambda call: call.data.startswith('stars_'))
def handle_telegram_stars_selection(call):
    selected_pkg = call.data.split('_', 1)[1]
    price = telegram_stars[selected_pkg]
    text = escape_markdown(
        f"⭐ Siz *{selected_pkg}* paketini tanladingiz.\n\n"
        f"💵 Narxi: *{price:,} UZS.*\n\n"
        f"🛒 Ushbu paketni sotib olish uchun admin bilan bog'laning:\n{ADMIN_USERNAME}"
    )
    bot.send_message(
        call.message.chat.id,
        text,
        reply_markup=back_to_main_menu(),
        parse_mode='MarkdownV2'
    )

# UC paketini tanlash
@bot.callback_query_handler(func=lambda call: call.data.startswith('uc_'))
def handle_uc_package_selection(call):
    selected_pkg = call.data.split('_', 1)[1]
    price = uc_packages[selected_pkg]
    text = escape_markdown(
        f"🎮 Siz *{selected_pkg}* paketini tanladingiz.\n\n"
        f"💵 Narxi: *{price:,} so'm.*\n\n"
        f"🛒 Ushbu paketni sotib olish uchun admin bilan bog'laning:\n{ADMIN_USERNAME}"
    )
    bot.send_message(
        call.message.chat.id,
        text,
        reply_markup=back_to_main_menu(),
        parse_mode='MarkdownV2'
    )

# Telegram Premium paketini tanlash
@bot.callback_query_handler(func=lambda call: call.data.startswith('premium_'))
def handle_premium_selection(call):
    selected_pkg = call.data.split('_', 1)[1]
    price = telegram_premium[selected_pkg]
    text = escape_markdown(
        f"✨ Siz *{selected_pkg}* paketini tanladingiz.\n\n"
        f"💵 Narxi: *{price:,} UZS.*\n\n"
        f"🛒 Ushbu paketni sotib olish uchun admin bilan bog'laning:\n{ADMIN_USERNAME}"
    )
    bot.send_message(
        call.message.chat.id,
        text,
        reply_markup=back_to_main_menu(),
        parse_mode='MarkdownV2'
    )

# Bosh menyuga o'tish inline klaviaturasi
@bot.callback_query_handler(func=lambda call: call.data == 'back_to_main')
def go_back(call):
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=escape_markdown("🔙 Bosh menyuga qaytdingiz. 📋 Quyidagi xizmatlardan birini tanlang:"),
        reply_markup=main_menu(),
        parse_mode='MarkdownV2'
    )

print("🤖 Bot Ishlamoqda...")

# Botni ishga tushurish
bot.polling(none_stop=True)

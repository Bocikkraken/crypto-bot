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
    "Solana (SOL Network)": "2YiYDkEoYG4yaeVAVQgoR6yuD6RYEazRmUm6o21BBFpG"
}

withdraw_methods = [
    "Czek BLIK", "Kod BLIK", "Przelew bankowy", "PayPal", "Revolut", "ZEN"
]

# --- HANDLERY ---
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "👋 Witaj! Ten bot pozwala Ci wpłacić kryptowaluty i zlecić wypłatę.\n\n" +
        "/deposit - Wpłata krypto\n/withdraw - Wypłata\n/balance - Saldo"
    )

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

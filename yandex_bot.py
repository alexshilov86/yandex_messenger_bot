from yandex_messenger_bot import Bot

TOKEN = "y0__wgBEOK5hvoIGJaREyCI1IKXGCZ-TzV1lOeL4Oek0EK-fGA7r-xb"
bot = Bot(TOKEN)

async def process_update(update):
    msg = update.get("message")
    if not msg:
        return
    chat_id = msg["chat"]["id"]
    text = msg.get("text")
    if text:
        await bot.send_message(chat_id, text)

bot.polling(process_update)
"""Telegram headspace — connect this shell to Telegram."""
import os
try:
    from telegram.ext import Application, CommandHandler, MessageHandler, filters
    HAS_TELEGRAM = True
except:
    HAS_TELEGRAM = False

TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
APP = None

async def handle_message(update, context):
    """Route incoming messages to the agent loop."""
    text = update.message.text
    # Run through agent
    from agent import Agent
    a = Agent("telegram")
    a.walk("fleet_health")
    await update.message.reply_text(f"Shell received: {text[:100]}")

def start():
    global APP
    if not TOKEN:
        return {"error": "TELEGRAM_TOKEN not set"}
    if not HAS_TELEGRAM:
        return {"error": "python-telegram-bot not installed. pip install python-telegram-bot"}
    APP = Application.builder().token(TOKEN).build()
    APP.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    APP.run_polling(drop_pending_updates=True)
    return {"status": "running"}

def stop():
    global APP
    if APP: APP.stop()
    return {"status": "stopped"}

def status():
    return {"running": APP is not None, "token_set": bool(TOKEN)}

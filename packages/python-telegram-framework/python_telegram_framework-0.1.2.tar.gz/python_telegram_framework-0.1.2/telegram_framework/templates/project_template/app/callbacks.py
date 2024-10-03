from telegram import Update
from telegram.ext import ContextTypes

async def _start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(f"Hi {user.name}!")
    
async def _help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_html(
        f"These are the available commands:\n \
        &#8226; \"<b>/start</b>\"\n \
        &#8226; \"<b>/help</b>\""
    )

async def _echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)
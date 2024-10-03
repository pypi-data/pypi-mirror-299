from telegram.ext import filters, CommandHandler, MessageHandler

from .callbacks import _start, _help, _echo

handlers = [
    CommandHandler('start', _start),
    CommandHandler('help', _help),
    MessageHandler(filters.TEXT & ~filters.COMMAND, _echo),
]

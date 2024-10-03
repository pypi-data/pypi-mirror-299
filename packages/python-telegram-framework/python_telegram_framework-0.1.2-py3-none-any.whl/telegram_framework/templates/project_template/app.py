import logging

from telegram_framework.conf.utils import initialize_settings
from telegram_framework.conf import settings
from telegram_framework.core.app import BotApp

initialize_settings(__file__)

logging.basicConfig(
    format=settings.LOGGING_FORMAT,
    level=logging.DEBUG if settings.DEBUG else settings.LOGGING_LEVEL
)
logger = logging.getLogger(__name__)

def main() -> None:
    """Start the bot."""
    app = BotApp()
    app.run()


if __name__ == "__main__":
    main()

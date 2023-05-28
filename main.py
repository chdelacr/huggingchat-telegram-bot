import logging

from dotenv import load_dotenv
from hughchat_helper import hughChatHelper
from sftp_handler import sftpLoadCookies
from telegram_bot import huggingChatTelegramBot

# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

def main():
    # Load environment variables
    load_dotenv()
    
    sftpLoadCookies()
    
    telegram_bot = huggingChatTelegramBot(hughChatHelper())
    telegram_bot.run()

if __name__ == '__main__':
    main()

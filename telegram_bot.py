import logging
import os

from hughchat_helper import hughChatHelper
from telegram import BotCommand, Update, constants
from telegram.ext import Application, ApplicationBuilder, CommandHandler, ContextTypes, filters, MessageHandler

logger = logging.getLogger("__main__.telegram_bot")

# Commands
HELP_COMMAND = "help"
RESET_COMMAND = "reset"
LINK_COMMAND = "link"

class huggingChatTelegramBot:
    def __init__(self, hughchat: hughChatHelper):
        self.telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.allowed_telegram_user_id = int(os.getenv("ALLOWED_TELEGRAM_USER_ID"))

        self.commands = [
            BotCommand(f"/{HELP_COMMAND}", "Shows help menu"),
            BotCommand(f"/{RESET_COMMAND}", "Reset conversation"),
            # Disabled for now since the conversation doesn't show previous messages and writing a follow up message returns a 500 error
            # BotCommand(f"/{LINK_COMMAND}", "Current conversation link")
        ]
        
        self.hughchat = hughchat
    
    async def help(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
        if update.effective_user.id == self.allowed_telegram_user_id:
            commands_description = [f"{command.command} - {command.description}" for command in self.commands]
            help_text = (
                    f"Hi, {update.effective_user.first_name}. I'm a Telegram bot that responds utilizing the HuggingChat AI chat model..\n\n" +
                    "Available commands:\n" +
                    '\n'.join(commands_description)
            )
            await update.message.reply_text(help_text)
        else:
            logger.warning("Unauthorized access attempt")
            await update.message.reply_text("Sorry, you are not authorized to use this command.")
    
    async def reset(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id == self.allowed_telegram_user_id:
            self.hughchat.delete_last_conversation()
            self.hughchat.start_new_conversation()

            logger.info("Sending welcome message")
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Conversation reset. Feel free to send any message."
            )
        else:
            logger.warning("Unauthorized access attempt")
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Sorry, you are not authorized to use this command."
            )
            
    """async def link(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id == self.allowed_telegram_user_id:
            logger.info("Sending conversation link")
            conversation_link = self.hughchat.get_conversation_link()
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"This is the link of the current conversation: {conversation_link}. You can click on the link to continue this conversation on the web.",
                disable_web_page_preview=True
            )
        else:
            logger.warning("Unauthorized access attempt")
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Sorry, you are not authorized to use this command."
            )"""
    
    async def message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id == self.allowed_telegram_user_id:
            logger.info("Sending user message to HuggingChat")
            user_message = update.message.text
            
            chat_id = update.effective_chat.id
            await update.effective_message.reply_chat_action(
                    message_thread_id=chat_id,
                    action=constants.ChatAction.TYPING
                )

            logger.info("Getting response from HuggingChat")
            response = self.hughchat.chatbot.chat(user_message, is_retry=True)
            
            try:
                logger.info("Sending response to Telegram bot")
                await context.bot.send_message(
                                    chat_id=chat_id,
                                    text=response,
                                    parse_mode=constants.ParseMode.MARKDOWN
                                )
            except Exception:
                await context.bot.send_message(
                                    chat_id=chat_id,
                                    text=response
                                )
        else:
            logger.warning("Unauthorized access attempt")
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Sorry, you are not authorized to send messages to this bot."
            )
            
    async def post_init(self, application: Application) -> None:
        await application.bot.set_my_commands(self.commands)
    
    def run(self):
        application = ApplicationBuilder() \
            .token(self.telegram_bot_token) \
            .post_init(self.post_init) \
            .concurrent_updates(True) \
            .build()
            
        # Add command handlers
        application.add_handler(CommandHandler("start", self.help))
        application.add_handler(CommandHandler(HELP_COMMAND, self.help))
        application.add_handler(CommandHandler(RESET_COMMAND, self.reset))
        # application.add_handler(CommandHandler(LINK_COMMAND, self.link))
        application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self.message))
        
        logger.info("Initializing Telegram bot")
        application.run_polling()
import logging

from hugchat import hugchat

logger = logging.getLogger("__main__.hughchat_helper")

class hughChatHelper:
    def __init__(self):
        logger.info("Initializing HuggingChat chatbot")
        self.chatbot = hugchat.ChatBot(cookie_path="local_cookies.json")
        
    def delete_last_conversation(self):
        logger.info("Deleting last conversation")
        conversation_list = self.chatbot.get_conversation_list()
        self.chatbot.delete_conversation(conversation_list.pop())
        
    def start_new_conversation(self):
        logger.info("Creating a new conversation")
        id = self.chatbot.new_conversation()
        self.chatbot.change_conversation(id)
        
    def get_conversation_link(self):
        logger.info("Getting conversation link")
        id = self.chatbot.current_conversation
        return self.chatbot.share_conversation(id)
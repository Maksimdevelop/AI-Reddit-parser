from gigachat import GigaChat
from config.config import config

class GigaChatAPI:
   def __init__(self):
      self.giga = GigaChat(
         credentials=config.AI_API_KEY,
         base_url="https://api.giga.chat/v1",
         scope="GIGACHAT_API_PERS",
         model=config.AI_MODEL,
         verify_ssl_certs=False
      )
   def Message(self, payload):
      response = self.giga.chat(payload)
      return response

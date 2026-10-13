import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        # 1. Считываем окружение
        self.DB_ENGINE = os.getenv("DB_ENGINE", "sqlite") # Для локального исследования рынка SQLite более чем хватит
        self.DB_NAME = os.getenv("DB_NAME", "market_research.db")
        
        self.AI_PLATFORM = os.getenv("AI_PLATFORM")
        self.AI_API_KEY = os.getenv("AI_API_KEY")
        self.AI_MODEL = os.getenv("AI_MODEL")
        self.SYSTEM_PROMPT_FILE_PATH = os.getenv("SYSTEM_PROMPT_FILE_PATH")

        # 2. Жёсткий Fail Fast на старте
        self._validate()

    def _validate(self):
        required_vars = {
            "AI_API_KEY": self.AI_API_KEY,
            "AI_MODEL": self.AI_MODEL,
            "SYSTEM_PROMPT_FILE_PATH": self.SYSTEM_PROMPT_FILE_PATH,
        }
        
        # Проверяем наличие ключей
        for var_name, value in required_vars.items():
            if not value:
                raise ValueError(f"❌ Критическая ошибка: Конфиг не собран! Переменная {var_name} отсутствует в .env")

        # Проверяем, что промпт реально лежит на диске
        if not os.path.exists(self.SYSTEM_PROMPT_FILE_PATH):
            raise FileNotFoundError(f"❌ Файл с системным промптом не найден: {self.SYSTEM_PROMPT_FILE_PATH}")

config = Config()
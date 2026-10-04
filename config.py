import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    AGENTS_DIR = os.path.join(BASE_DIR, "generated_agents")
    DB_PATH = os.path.join(BASE_DIR, "agent_registry.db")

    @classmethod
    def validate(cls):
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set. Please check your .env file or environment variables.")
        if not os.path.exists(cls.AGENTS_DIR):
            os.makedirs(cls.AGENTS_DIR)

Config.validate()

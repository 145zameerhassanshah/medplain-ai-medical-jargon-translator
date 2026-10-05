import os
from dotenv import load_dotenv


load_dotenv()


APP_NAME = "MedPlain AI"
APP_TAGLINE = "Clinical language made clear"


OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY"
)

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


DEFAULT_MODEL = "nvidia/nemotron-3-ultra:free"


SUPPORTED_LANGUAGES = [
    "English",
    "Urdu",
    "Roman Urdu",
    "Arabic",
]


READING_LEVELS = [
    "Simple",
    "Standard",
    "Detailed",
]
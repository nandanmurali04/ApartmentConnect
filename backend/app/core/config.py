import os
from pathlib import Path
from dotenv import load_dotenv

# Get backend folder
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load backend/.env
load_dotenv(BASE_DIR / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60)
)

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
print("BASE_DIR:", BASE_DIR)
print("ENV EXISTS:", (BASE_DIR / ".env").exists())
print("CONFIG EMAIL:", repr(EMAIL_ADDRESS))
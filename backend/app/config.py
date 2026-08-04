import os
from pathlib import Path

# Finds the 'backend' folder path automatically
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'textile_waste_platform_super_secret_key_2024_xK9mP2nQ')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 # 24 hours

# Absolute path to backend/textile_waste.db
DATABASE_URL = f"sqlite:///{BASE_DIR / 'textile_waste.db'}" 
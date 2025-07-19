from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv('API_KEY', 'default123')  # ← Lee esto del archivo .env

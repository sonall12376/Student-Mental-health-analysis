import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

class Settings:
    """
    Application configuration settings loaded from environment or defaults.
    """
    MONGODB_URI: str = os.getenv("MONGODB_URI", "")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "mindease_super_secret_key_change_me_in_production_12345")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
    
    # Path to saved model files
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MODEL_PATH: str = os.path.join(BASE_DIR, "models", "best_model.joblib")
    FEATURES_PATH: str = os.path.join(BASE_DIR, "models", "model_features.json")

settings = Settings()

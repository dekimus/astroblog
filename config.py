import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'astroblog.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(BASE_DIR,"static", "uploads")
    ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "tif", "tiff"}
    MAX_CONTENT_LENGTH = 25 * 1024 * 1024  # 25 
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    THUMBNAIL_SIZE = (600, 600)
    DISPLAY_SIZE = (1920, 1920)  
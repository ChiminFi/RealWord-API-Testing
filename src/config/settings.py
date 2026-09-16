import os

from dotenv import load_dotenv

load_dotenv()


BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
REQUEST_CONNECT_TIMEOUT = 5
REQUEST_READ_TIMEOUT = 30
REQUEST_TIMEOUT = (REQUEST_CONNECT_TIMEOUT, REQUEST_READ_TIMEOUT)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_SSLMODE = os.getenv("DB_SSLMODE", "prefer")

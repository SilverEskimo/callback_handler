import os
from dotenv import load_dotenv
from src.databases.mongo import MongoDB
from src.databases.postgres import PostgresDB
from src.logs.logger_config import logger
from src.exceptions import ValidationError, DatabaseUnsupportedError

# Load environment variables from .env file
load_dotenv()


DB_CLASS_MAP = {
    'postgres': PostgresDB,
    'mongodb': MongoDB,
}

PLUGINS = os.getenv("PLUGINS").split(",")
DB_TYPE = os.getenv("DB_TYPE")
# For TxID Validation Plugin
DB_TABLE = os.getenv("DB_TABLE")
DB_COLUMN = os.getenv("DB_COLUMN")
DB_USER = os.getenv("DB_USER")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
COSIGNER_PUBLIC_KEY_PATH = os.getenv('COSIGNER_PUBLIC_KEY_PATH')
CALLBACK_PRIVATE_KEY_PATH = os.getenv('CALLBACK_PRIVATE_KEY_PATH')
EXTRA_SIGNATURE_PUBLIC_KEY_PATH = os.getenv('EXTRA_SIGNATURE_PUBLIC_KEY_PATH')
SERVER_PORT = 8000

DB_CONFIG = {
    "user": DB_USER,
    "host": DB_HOST,
    "password": DB_PASSWORD,
    "port": DB_PORT,
    "database": DB_NAME
}


def validate_db_config() -> None:
    if DB_TYPE not in DB_CLASS_MAP:
        if not (DB_TYPE is None or DB_TYPE == ""):
            raise DatabaseUnsupportedError(f"Unsupported DB type: {DB_TYPE}")
        else:
            if "txid_validation" in PLUGINS:
                raise ValueError(f"txid_validation plugin requires a valid DB setup")


def run_validations() -> None:
    try:
        validate_db_config()
        logger.info("Completed all validations")
    except Exception as e:
        raise ValidationError(f"Failed to validate settings.py with the following error {e}")






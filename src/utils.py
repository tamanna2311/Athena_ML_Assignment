import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_logging(name=__name__):
    """
    Sets up a logger with a standard format.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

def get_api_key():
    """
    Retrieves the Google API key from environment variables.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        # Fallback or warning
        pass
    return api_key

def ensure_dir(directory):
    """
    Ensures that a directory exists.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

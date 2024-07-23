from dotenv import load_dotenv
import os

def load_config():
    """Loads environment variables from the .env file."""
    load_dotenv()
    return {
        'DISCORD_TOKEN': os.getenv('DISCORD_TOKEN'),
        'DATABASE_URL': os.getenv('DATABASE_URL'),
        'REDIS_URL': os.getenv('REDIS_URL'),
        'DEFAULT_PREFIX': os.getenv('DEFAULT_PREFIX', '!')  # Default prefix if not specified
    }

def get_config():
    """Returns a dictionary containing all the configuration settings."""
    return load_config()
import os
from dotenv import load_dotenv
from typing import Union

# Load environment variables from .env file
load_dotenv()


def validate_env_var(var_name: str, default_value: Union[str, int, None] = None) -> str:
    """Validate the environment variable."""
    v = os.getenv(var_name)
    if v is None:
        if default_value is not None:
            return str(default_value)
        raise ValueError(f"Missing environment variable: {var_name}")
    return v


class Settings:
    def __init__(self):
        # API Configuration
        self.api_host = validate_env_var("API_HOST", "localhost")
        self.api_port = int(validate_env_var("API_PORT", "9000"))
        self.api_prefix = validate_env_var("API_PREFIX", "iot_management")
        
        # Database Configuration
        self.db_host = validate_env_var("DB_HOST", "localhost")
        self.db_port = int(validate_env_var("DB_PORT", "5432"))
        self.db_name = validate_env_var("DB_NAME", "iot_manager")
        self.db_user = validate_env_var("DB_USER", "postgres")
        self.db_pass = validate_env_var("DB_PASS")
        self.db_schema = validate_env_var("DB_SCHEMA", "iot_manager")
        
    @property
    def database_url(self) -> str:
        """Construct database URL from individual components"""
        return f"postgresql://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"


settings = Settings()

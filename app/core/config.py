import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import ConfigDict
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    # Azure Search Configuration
    azure_search_service_name: str = os.getenv("AZURE_SEARCH_SERVICE_NAME", "")
    azure_search_api_key: str = os.getenv("AZURE_SEARCH_API_KEY", "")
    azure_search_index_name: str = os.getenv(
        "AZURE_SEARCH_INDEX_NAME", "azureblob-index"
    )

    # Azure Storage Configuration
    azure_storage_connection_string: str = os.getenv(
        "AZURE_STORAGE_CONNECTION_STRING", ""
    )

    # Azure Vision Configuration
    azure_vision_key: str = os.getenv("AZURE_VISION_KEY", "")
    azure_vision_endpoint: str = os.getenv("AZURE_VISION_ENDPOINT", "")

    # Application Settings
    app_name: str = "Furniture Search Engine"
    debug: bool = True

    model_config = ConfigDict(
        env_file=".env",
        extra="ignore",  # to allow extra fields?
        case_sensitive=True,
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()

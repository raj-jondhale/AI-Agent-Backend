"""
Configuration management for the AI Agent
Centralized settings and API key management
"""

import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()


class Config:
    """Application configuration"""
    
    # API Keys
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENWEATHER_API_KEY: Optional[str] = os.getenv("OPENWEATHER_API_KEY")
    NEWS_API_KEY: Optional[str] = os.getenv("NEWS_API_KEY")
    
    # OpenAI Settings
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    OPENAI_TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
    OPENAI_MAX_TOKENS: int = int(os.getenv("OPENAI_MAX_TOKENS", "500"))
    
    # Agent Settings
    MAX_MEMORY_SIZE: int = int(os.getenv("MAX_MEMORY_SIZE", "5"))
    
    # API Settings
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "10"))
    
    # Server Settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    @classmethod
    def validate(cls) -> dict:
        """
        Validate configuration and return status
        
        Returns:
            Dictionary with validation results
        """
        return {
            "openai_configured": cls.OPENAI_API_KEY is not None and len(cls.OPENAI_API_KEY) > 0,
            "weather_configured": cls.OPENWEATHER_API_KEY is not None and len(cls.OPENWEATHER_API_KEY) > 0,
            "news_configured": cls.NEWS_API_KEY is not None and len(cls.NEWS_API_KEY) > 0,
        }
    
    @classmethod
    def is_ready(cls) -> bool:
        """
        Check if minimum required configuration is present
        
        Returns:
            True if at least OpenAI API key is configured
        """
        validation = cls.validate()
        return validation["openai_configured"]


# Create a singleton instance
config = Config()


if __name__ == "__main__":
    # Test configuration
    print("Configuration Status:")
    print("-" * 50)
    validation = config.validate()
    
    for key, value in validation.items():
        status = "✅" if value else "❌"
        print(f"{status} {key}: {value}")
    
    print("\nConfiguration Values:")
    print("-" * 50)
    print(f"OpenAI Model: {config.OPENAI_MODEL}")
    print(f"Temperature: {config.OPENAI_TEMPERATURE}")
    print(f"Max Tokens: {config.OPENAI_MAX_TOKENS}")
    print(f"Max Memory Size: {config.MAX_MEMORY_SIZE}")
    print(f"Request Timeout: {config.REQUEST_TIMEOUT}s")
    print(f"Host: {config.HOST}")
    print(f"Port: {config.PORT}")
    print(f"Debug Mode: {config.DEBUG}")
    
    print("\nSystem Ready:", "✅" if config.is_ready() else "❌")

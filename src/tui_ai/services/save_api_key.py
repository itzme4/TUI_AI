import os
from dotenv import set_key
from pathlib import Path
ENV_PATH=Path.cwd()/".env"
def save_api_key(provider:str,api_key:str):
    provider_keys={
        "gemini":"GEMINI_API_KEY",
        "groq":"GROQ_API_KEY"
    }
    try:
        env_key=provider_keys.get(provider.lower())
        if not env_key:
            return ValueError(f"Invalid Provider:{provider}")
        if not api_key.strip():
            return ValueError("API key cannot be empty")
        ENV_PATH.touch(exist_ok=True)
        set_key(str(ENV_PATH),env_key,api_key.strip())
    except Exception as e:
        return e
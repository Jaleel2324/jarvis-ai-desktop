import time

from fastapi import APIRouter
from openai import OpenAI
from pydantic import BaseModel


router = APIRouter(
    prefix="/api/settings"
)

START_TIME = time.time()

OLLAMA_MODEL = "llama3.2"


class KeyUpdate(BaseModel):
    key_name: str
    key_value: str


class PreferencesUpdate(BaseModel):
    user_name: str = ""
    honorific: str = "sir"
    calendar_accounts: str = "local"


class OllamaTest(BaseModel):
    model: str = "llama3.2"


class VoiceTest(BaseModel):
    provider: str = "xtts"


preferences = {
    "user_name": "Jaleel",
    "honorific": "sir",
    "calendar_accounts": "local",
}


settings_store = {
    "OLLAMA_MODEL": OLLAMA_MODEL,
    "VOICE_PROVIDER": "xtts",
    "VOICE_ID": "Craig Gutsy",
}


@router.get("/status")
def settings_status():
    uptime_seconds = int(
        time.time() - START_TIME
    )

    ollama_accessible = False

    try:
        client = OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama",
        )

        client.models.list()

        ollama_accessible = True

    except Exception:
        ollama_accessible = False

    return {
        "ollama_accessible": ollama_accessible,
        "windows_calendar_accessible": False,
        "windows_notifications_accessible": True,
        "local_memory_accessible": True,
        "memory_count": 0,
        "task_count": 0,
        "server_port": 8000,
        "uptime_seconds": uptime_seconds,
        "env_keys_set": {
            "ollama": True,
            "voice_provider": True,
            "voice_id": True,
            "user_name": preferences["user_name"],
        },
    }


@router.get("/preferences")
def get_preferences():
    return preferences


@router.post("/preferences")
def save_preferences(
    data: PreferencesUpdate
):
    preferences["user_name"] = data.user_name
    preferences["honorific"] = data.honorific
    preferences["calendar_accounts"] = data.calendar_accounts

    return {
        "success": True,
        "preferences": preferences,
    }


@router.post("/keys")
def save_key(
    data: KeyUpdate
):
    settings_store[data.key_name] = data.key_value

    return {
        "success": True,
        "key_name": data.key_name,
    }


@router.post("/test-ollama")
def test_ollama(
    data: OllamaTest
):
    try:
        client = OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama",
        )

        response = client.chat.completions.create(
            model=data.model or OLLAMA_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": "Say online.",
                }
            ],
        )

        return {
            "valid": True,
            "response": response.choices[0].message.content,
        }

    except Exception as e:
        return {
            "valid": False,
            "error": str(e),
        }


@router.post("/test-voice")
def test_voice(
    data: VoiceTest
):
    provider = data.provider or "xtts"

    return {
        "valid": provider.lower() in [
            "xtts",
            "browser",
            "local",
        ],
        "provider": provider,
    }
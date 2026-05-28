import base64
import os

import requests


FISH_TTS_URL = "https://api.fish.audio/v1/tts"


def generate_tts_base64(text):
    api_key = os.environ.get("FISH_API_KEY")
    reference_id = os.environ.get("FISH_REFERENCE_ID")

    if not api_key:
        return {
            "success": False,
            "error": "Missing FISH_API_KEY environment variable.",
            "text": text,
            "audio_base64": None,
        }

    if not reference_id:
        return {
            "success": False,
            "error": "Missing FISH_REFERENCE_ID environment variable.",
            "text": text,
            "audio_base64": None,
        }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "model": "s1",
    }

    payload = {
        "text": text,
        "reference_id": reference_id,
        "format": "mp3",
        "latency": "balanced",
        "speed": 1.0,
    }

    try:
        response = requests.post(
            FISH_TTS_URL,
            headers=headers,
            json=payload,
            timeout=120,
        )

        if response.status_code >= 400:
            return {
                "success": False,
                "error": f"Fish Audio error {response.status_code}: {response.text[:1000]}",
                "text": text,
                "audio_base64": None,
            }

        audio_base64 = base64.b64encode(response.content).decode("utf-8")

        return {
            "success": True,
            "error": None,
            "text": text,
            "audio_base64": audio_base64,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "text": text,
            "audio_base64": None,
        }


def encode_audio_file_base64(path):
    with open(path, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")
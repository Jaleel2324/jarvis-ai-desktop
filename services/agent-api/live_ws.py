import asyncio
import json
import uuid

from datetime import datetime
from typing import Any, Dict, List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from openai import OpenAI

from tts_engine import generate_tts_base64


router = APIRouter()

OLLAMA_MODEL = "llama3.2"

print(f"[jarvis] websocket model: {OLLAMA_MODEL}")

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)


class JarvisWebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

        print("[ws] client connected")

        await self.send_personal_message(
            websocket,
            {
                "type": "status",
                "state": "idle",
                "message": "JARVIS websocket online",
                "timestamp": datetime.now().isoformat(),
            },
        )

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

        print("[ws] client disconnected")

    async def send_personal_message(
        self,
        websocket: WebSocket,
        message: Dict[str, Any],
    ):
        print("[ws] sending:", message.get("type"))

        await websocket.send_text(
            json.dumps(message)
        )


manager = JarvisWebSocketManager()


async def send_status(
    websocket: WebSocket,
    state: str
):
    await manager.send_personal_message(
        websocket,
        {
            "type": "status",
            "state": state,
            "timestamp": datetime.now().isoformat(),
        },
    )


async def send_text(
    websocket: WebSocket,
    text: str
):
    await manager.send_personal_message(
        websocket,
        {
            "type": "text",
            "text": text,
            "timestamp": datetime.now().isoformat(),
        },
    )


async def send_audio_fallback(
    websocket: WebSocket,
    text: str
):
    print("[audio] generating audio for response")

    result = await asyncio.to_thread(
        generate_tts_base64,
        text,
    )

    if isinstance(result, dict):
        audio_base64 = (
            result.get("audio_base64")
            or result.get("data")
            or result.get("audio")
        )

        if not audio_base64:
            print("[audio] no audio generated:", result.get("error"))

    else:
        audio_base64 = result

    if not audio_base64:
        await manager.send_personal_message(
            websocket,
            {
                "type": "text",
                "text": (
                    "Voice audio was not generated yet, "
                    "but the text response is working."
                ),
                "timestamp": datetime.now().isoformat(),
            },
        )
        return

    print("[audio] sending base64 audio length:", len(audio_base64))

    await manager.send_personal_message(
        websocket,
        {
            "type": "audio",
            "data": audio_base64,
            "text": text,
            "timestamp": datetime.now().isoformat(),
        },
    )


def generate_ollama_response(user_message: str):
    print("[ollama] prompt:", user_message)

    response = client.chat.completions.create(
        model=OLLAMA_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are JARVIS, a cinematic Windows 11 desktop AI assistant. "
                    "You run locally through Ollama using llama3.2. "
                    "Be fast, direct, intelligent, concise, and action-focused. "
                    "You help with coding, planning, automation, Windows tasks, "
                    "software engineering, debugging, and project generation."
                ),
            },
            {
                "role": "user",
                "content": user_message,
            },
        ],
    )

    answer = response.choices[0].message.content or ""

    print("[ollama] response:", answer[:300])

    return answer


async def handle_transcript(
    websocket: WebSocket,
    text: str
):
    request_id = str(uuid.uuid4())

    print("[transcript] final:", text)

    await send_status(
        websocket,
        "thinking"
    )

    try:
        response_text = await asyncio.to_thread(
            generate_ollama_response,
            text,
        )

        await send_status(
            websocket,
            "speaking"
        )

        await send_text(
            websocket,
            response_text
        )

        await send_audio_fallback(
            websocket,
            response_text
        )

        await send_status(
            websocket,
            "idle"
        )

    except Exception as e:
        print("[ws] handle transcript error:", str(e))

        await manager.send_personal_message(
            websocket,
            {
                "type": "text",
                "request_id": request_id,
                "text": f"JARVIS error: {str(e)}",
                "timestamp": datetime.now().isoformat(),
            },
        )

        await send_status(
            websocket,
            "idle"
        )


async def handle_fix_self(
    websocket: WebSocket
):
    task_id = str(uuid.uuid4())

    await manager.send_personal_message(
        websocket,
        {
            "type": "task_spawned",
            "task_id": task_id,
            "prompt": "Self-repair mode requested.",
            "timestamp": datetime.now().isoformat(),
        },
    )

    await send_status(
        websocket,
        "working"
    )

    summary = (
        "Self-repair mode is connected. "
        "Current Windows/Ollama version can inspect logs, backups, "
        "project files, and safe refactor systems."
    )

    await manager.send_personal_message(
        websocket,
        {
            "type": "task_complete",
            "task_id": task_id,
            "status": "ready",
            "summary": summary,
            "timestamp": datetime.now().isoformat(),
        },
    )

    await send_text(
        websocket,
        summary
    )

    await send_audio_fallback(
        websocket,
        summary
    )

    await send_status(
        websocket,
        "idle"
    )


@router.websocket("/ws/voice")
async def voice_websocket(
    websocket: WebSocket
):
    await manager.connect(websocket)

    try:
        while True:
            raw_data = await websocket.receive_text()

            print("[ws] raw received:", raw_data[:500])

            try:
                data = json.loads(raw_data)

            except Exception:
                data = {
                    "type": "transcript",
                    "text": raw_data,
                    "isFinal": True,
                }

            message_type = data.get("type")

            print("[ws] message type:", message_type)
            print("[ws] data:", data)

            if message_type == "ping":
                await manager.send_personal_message(
                    websocket,
                    {
                        "type": "pong",
                        "timestamp": datetime.now().isoformat(),
                    },
                )

            elif message_type == "transcript":
                text = str(
                    data.get("text", "")
                ).strip()

                is_final = bool(
                    data.get("isFinal", True)
                )

                print("[ws] transcript text:", text)
                print("[ws] transcript final:", is_final)

                if text and is_final:
                    await handle_transcript(
                        websocket,
                        text
                    )

                elif not text:
                    await send_text(
                        websocket,
                        "Empty transcript received.",
                    )

            elif message_type == "fix_self":
                await handle_fix_self(
                    websocket
                )

            elif message_type == "voice_start":
                await send_status(
                    websocket,
                    "listening"
                )

            elif message_type == "voice_end":
                await send_status(
                    websocket,
                    "idle"
                )

            else:
                await send_text(
                    websocket,
                    f"Unknown websocket message type: {message_type}",
                )

    except WebSocketDisconnect:
        manager.disconnect(websocket)

    except Exception as e:
        manager.disconnect(websocket)

        print(
            f"WebSocket error: {e}"
        )


@router.websocket("/ws/jarvis")
async def jarvis_websocket_compat(
    websocket: WebSocket
):
    await voice_websocket(
        websocket
    )
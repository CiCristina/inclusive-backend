import httpx
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pydantic import BaseModel

from core.config import settings
from core.deps import get_current_user
from models.user import User

router = APIRouter(prefix="/ai", tags=["ai"])

SUPPORTED_AUDIO_TYPES = {
    "audio/wav",
    "audio/mpeg",
    "audio/mp4",
    "audio/webm",
    "audio/ogg",
    "audio/x-wav",
}


class TranscribeResponse(BaseModel):
    text: str


@router.post("/transcribe", response_model=TranscribeResponse)
async def transcribe_audio(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    if file.content_type not in SUPPORTED_AUDIO_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported audio format: {file.content_type}. "
                   f"Supported: {', '.join(SUPPORTED_AUDIO_TYPES)}",
        )

    audio_bytes = await file.read()
    if len(audio_bytes) == 0:
        raise HTTPException(status_code=400, detail="Audio file is empty")

    if not settings.AZURE_SPEECH_KEY or not settings.AZURE_SPEECH_ENDPOINT:
        raise HTTPException(
            status_code=503,
            detail="Azure Speech-to-Text is not configured yet",
        )

    # TODO (Mingyu): Confirm the correct path to append to AZURE_SPEECH_ENDPOINT
    # for the transcription call. Current guess based on Azure AI Foundry patterns:
    #
    #   Option A (Azure AI Speech):
    #     path = "/speechtotext/transcriptions:transcribe?api-version=2024-11-15"
    #
    #   Option B (Whisper via Azure OpenAI):
    #     path = "/openai/deployments/<deployment-name>/audio/transcriptions?api-version=2024-02-01"
    #
    # Also confirm:
    #   - Should the audio be sent as multipart/form-data or base64 JSON?
    #   - What is the exact field name for the transcribed text in the response JSON?
    #   - Does the API accept a language parameter? (frontend uses pt-BR, en-US, es-ES)

    azure_url = settings.AZURE_SPEECH_ENDPOINT + "/speechtotext/transcriptions:transcribe?api-version=2024-11-15"

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            azure_url,
            headers={"api-key": settings.AZURE_SPEECH_KEY},
            files={"audio": (file.filename, audio_bytes, file.content_type)},
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=f"Azure Speech API error: {response.status_code} — {response.text}",
        )

    data = response.json()

    # TODO (Mingyu): Confirm the field name for the transcribed text in the response.
    # Common options: "text", "transcript", "combinedPhrases[0].text"
    transcribed_text = (
        data.get("text")
        or data.get("transcript")
        or data.get("combinedPhrases", [{}])[0].get("text", "")
    )

    if not transcribed_text:
        raise HTTPException(status_code=502, detail="Azure returned an empty transcription")

    return TranscribeResponse(text=transcribed_text)

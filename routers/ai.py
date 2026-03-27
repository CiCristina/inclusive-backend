import asyncio
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from pydantic import BaseModel

import azure.cognitiveservices.speech as speech_sdk

from core.config import settings
from core.deps import get_current_user
from models.user import User

router = APIRouter(prefix="/ai", tags=["ai"])

SUPPORTED_AUDIO_TYPES = {
    "audio/wav",
    "audio/x-wav",
    "audio/mpeg",
    "audio/mp4",
    "audio/webm",
    "audio/ogg",
}

# Languages supported by the frontend (i18n)
SUPPORTED_LANGUAGES = {"pt-BR", "en-US", "es-ES"}


class TranscribeResponse(BaseModel):
    text: str


@router.post("/transcribe", response_model=TranscribeResponse)
async def transcribe_audio(
    file: UploadFile = File(...),
    language: str = Query(default="pt-BR", description="BCP-47 language code, e.g. pt-BR, en-US, es-ES"),
    current_user: User = Depends(get_current_user),
):
    if file.content_type not in SUPPORTED_AUDIO_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported audio format '{file.content_type}'. "
                   f"Supported: {', '.join(SUPPORTED_AUDIO_TYPES)}",
        )

    if language not in SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported language '{language}'. "
                   f"Supported: {', '.join(SUPPORTED_LANGUAGES)}",
        )

    if not settings.AZURE_SPEECH_KEY or not settings.AZURE_SPEECH_REGION:
        raise HTTPException(
            status_code=503,
            detail="Azure Speech-to-Text is not configured yet (missing KEY or REGION)",
        )

    audio_bytes = await file.read()
    if not audio_bytes:
        raise HTTPException(status_code=400, detail="Audio file is empty")

    # Run the blocking SDK call in a thread so it doesn't freeze the async server
    text = await asyncio.to_thread(_transcribe_with_sdk, audio_bytes, language)
    return TranscribeResponse(text=text)


def _transcribe_with_sdk(audio_bytes: bytes, language: str) -> str:
    """
    Synchronous transcription using the Azure Speech SDK.
    Adapted from Mingyu's code — uses PushAudioInputStream so we don't
    need to write the uploaded file to disk.
    """
    speech_config = speech_sdk.SpeechConfig(
        subscription=settings.AZURE_SPEECH_KEY,
        region=settings.AZURE_SPEECH_REGION,
    )
    speech_config.speech_recognition_language = language

    # Feed audio bytes directly into the recognizer (no temp file needed)
    stream = speech_sdk.audio.PushAudioInputStream()
    stream.write(audio_bytes)
    stream.close()

    audio_config = speech_sdk.audio.AudioConfig(stream=stream)
    recognizer = speech_sdk.SpeechRecognizer(
        speech_config=speech_config,
        audio_config=audio_config,
    )

    result = recognizer.recognize_once_async().get()

    if result.reason == speech_sdk.ResultReason.RecognizedSpeech:
        return result.text

    if result.reason == speech_sdk.ResultReason.NoMatch:
        raise HTTPException(status_code=422, detail="Speech could not be recognized in the audio")

    if result.reason == speech_sdk.ResultReason.Canceled:
        details = speech_sdk.CancellationDetails.from_result(result)
        raise HTTPException(
            status_code=502,
            detail=f"Azure Speech canceled: {details.reason} — {details.error_details}",
        )

    raise HTTPException(status_code=502, detail="Unexpected response from Azure Speech")

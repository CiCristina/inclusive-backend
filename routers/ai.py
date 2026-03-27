from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pydantic import BaseModel

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

    # TODO: Replace this block with the Azure Speech-to-Text integration.
    #
    # Your teammate should:
    #   1. Add to .env:
    #        AZURE_SPEECH_KEY=<key>
    #        AZURE_SPEECH_REGION=<region>
    #   2. Add to requirements.txt:
    #        azure-cognitiveservices-speech
    #   3. Add to core/config.py:
    #        AZURE_SPEECH_KEY: str = ""
    #        AZURE_SPEECH_REGION: str = ""
    #   4. Replace this stub with the Azure SDK call, e.g.:
    #
    #        import azure.cognitiveservices.speech as speechsdk
    #        speech_config = speechsdk.SpeechConfig(
    #            subscription=settings.AZURE_SPEECH_KEY,
    #            region=settings.AZURE_SPEECH_REGION,
    #        )
    #        audio_input = speechsdk.audio.PushAudioInputStream()
    #        audio_input.write(audio_bytes)
    #        audio_input.close()
    #        audio_config = speechsdk.audio.AudioConfig(stream=audio_input)
    #        recognizer = speechsdk.SpeechRecognizer(
    #            speech_config=speech_config, audio_config=audio_config
    #        )
    #        result = recognizer.recognize_once()
    #        transcribed_text = result.text
    #
    # ── STUB (remove when Azure is integrated) ───────────────────────────────
    transcribed_text = (
        "[Azure Speech-to-Text not yet configured] "
        f"Received {len(audio_bytes)} bytes from user {current_user.id}"
    )
    # ─────────────────────────────────────────────────────────────────────────

    return TranscribeResponse(text=transcribed_text)

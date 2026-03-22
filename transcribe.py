import os
import sys
from groq import Groq
from config import GROQ_API_KEY, WHISPER_MODEL


def transcribe_audio(audio_file_path: str) -> str:
    """
    Transcribe audio file using Groq Whisper API.
    
    Args:
        audio_file_path: Path to the audio file to transcribe
        
    Returns:
        Transcribed text as string
    """
    if not os.path.exists(audio_file_path):
        raise FileNotFoundError(f"Audio file not found: {audio_file_path}")

    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not set in .env file")

    client = Groq(api_key=GROQ_API_KEY)

    print(f"🎙 Transcribing: {audio_file_path}")
    print("⏳ Please wait...")

    with open(audio_file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model=WHISPER_MODEL,
            file=audio_file,
            response_format="text"
        )

    print("✅ Transcription complete!")
    return transcription


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python transcribe.py <audio_file>")
        print("Example: python transcribe.py /tmp/voice_recording.wav")
        sys.exit(1)

    audio_path = sys.argv[1]

    try:
        result = transcribe_audio(audio_path)
        print("\n--- Transcript ---")
        print(result)
        print("------------------")
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"❌ Config error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

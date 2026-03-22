import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Whisper settings
WHISPER_MODEL = "whisper-large-v3"

# Obsidian settings
OBSIDIAN_VAULT_PATH = os.path.expanduser("~/ObsidianVault")
NOTES_FOLDER = "Voice Notes"

# Git settings
AUTO_GIT_COMMIT = True

# Audio settings
RECORDING_FILENAME = "/tmp/voice_recording.wav"
SAMPLE_RATE = 16000
CHANNELS = 1

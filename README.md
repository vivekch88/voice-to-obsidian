# voice-to-obsidian

🎙 Voice to structured Obsidian notes pipeline using Groq Whisper + Claude

## Overview

Speak your thoughts, get back a clean structured Markdown note — automatically saved to your Obsidian vault and committed to Git.
```
Your voice → sox (record) → Groq Whisper (transcribe) → Claude API (structure) → Obsidian vault (.md) → Git commit
```

## Tech Stack

- [Groq Whisper API](https://console.groq.com) — cloud speech to text (free tier)
- [Anthropic Claude API](https://anthropic.com) — note structuring
- [uv](https://github.com/astral-sh/uv) — Python package management
- [sox](https://sox.sourceforge.net) — audio recording on macOS
- [Obsidian](https://obsidian.md) — note taking
- Python 3.13

## Why Groq instead of local Whisper?

- macOS 15 Intel (x86_64) is not yet supported by PyTorch or onnxruntime
- Groq runs Whisper in the cloud — free tier, blazing fast, no local install headaches
- Same accuracy as running locally

## Prerequisites

- macOS (Intel or Apple Silicon)
- Python 3.13+
- Homebrew
- Obsidian installed
- Groq API key (free) — [console.groq.com](https://console.groq.com)
- Anthropic API key — [console.anthropic.com](https://console.anthropic.com)

## Installation

### 1. Install Obsidian
```bash
brew install --cask obsidian
```

### 2. Install uv
```bash
brew install uv
```

### 3. Install sox (audio recording)
```bash
brew install sox
```

### 4. Clone the repo
```bash
git clone https://github.com/vivekch88/voice-to-obsidian.git
cd voice-to-obsidian
```

### 5. Create virtual environment
```bash
uv venv --python 3.13
source .venv/bin/activate
```

### 6. Install dependencies
```bash
uv add groq anthropic python-dotenv setuptools
```

### 7. Set up environment variables
```bash
cp .env.example .env
# Edit .env and add your API keys
```

Your `.env` file should look like:
```
ANTHROPIC_API_KEY=your_anthropic_key_here
GROQ_API_KEY=your_groq_key_here
```

### 8. Set up Obsidian vault
Open Obsidian and create a new vault at:
```
~/ObsidianVault
```

Then create these folders inside it:
```
~/ObsidianVault/
├── Work/
│   ├── AWS/
│   ├── Databricks/
│   └── Projects/
├── Daily Notes/
├── Voice Notes/        ← auto-populated by this pipeline
├── Code Refs/
│   ├── MLflow/
│   ├── Spark/
│   └── Shell/
└── Resources/
```

### 9. Update config.py with your vault path
```python
OBSIDIAN_VAULT_PATH = "/Users/yourusername/ObsidianVault"
```

## Project Structure
```
voice-to-obsidian/
├── .venv/                  # virtual env (git ignored)
├── .env                    # API keys (git ignored)
├── .env.example            # template for env vars
├── .gitignore
├── .python-version         # pins Python 3.13
├── pyproject.toml          # uv dependencies
├── README.md
├── config.py               # vault path, model settings
├── record.sh               # records audio from mic via sox
├── transcribe.py           # sends audio to Groq Whisper
├── structure_note.py       # sends transcript to Claude API
└── voice_to_note.py        # main entry point — runs full pipeline
```

## Usage

### Run the full pipeline
```bash
source .venv/bin/activate
python voice_to_note.py
```

1. Script starts recording via sox
2. Speak your thoughts
3. Press `Ctrl+C` to stop recording
4. Groq Whisper transcribes the audio
5. Claude structures it into clean Markdown
6. Note saved to `~/ObsidianVault/Voice Notes/`
7. Auto committed to Git

### Run individual steps
```bash
# Just record audio
./record.sh

# Just transcribe an existing audio file
python transcribe.py /tmp/voice_recording.wav

# Just structure an existing transcript
python structure_note.py transcript.txt
```

## Configuration

Edit `config.py` to customise:

| Setting | Default | Description |
|---|---|---|
| `WHISPER_MODEL` | `whisper-large-v3` | Groq Whisper model |
| `OBSIDIAN_VAULT_PATH` | `~/ObsidianVault` | Path to your Obsidian vault |
| `NOTES_FOLDER` | `Voice Notes` | Folder inside vault for voice notes |
| `AUTO_GIT_COMMIT` | `True` | Auto commit after each note |
| `RECORDING_FILENAME` | `/tmp/voice_recording.wav` | Temp audio file location |
| `SAMPLE_RATE` | `16000` | Audio sample rate |

## Groq Whisper Models

| Model | Description |
|---|---|
| `whisper-large-v3` | Best accuracy (recommended) |
| `whisper-large-v3-turbo` | Faster, slightly lower accuracy |
| `distil-whisper-large-v2` | Fastest, good for quick notes |

## Dependencies

| Package | Version | Purpose |
|---|---|---|
| `groq` | 1.1.1 | Whisper transcription API |
| `anthropic` | 0.86.0 | Claude API for structuring notes |
| `python-dotenv` | 1.2.2 | Load API keys from .env |
| `setuptools` | 82.0.1 | Python build tools |

## Troubleshooting

### Python version issues on macOS
```bash
# Add to ~/.zshrc
export PATH="/usr/local/bin:$PATH"
alias python=python3.13
alias python3=python3.13
alias pip=pip3.13
source ~/.zshrc
```

### PyTorch/Whisper wheel errors on macOS 15 Intel
Use Groq API instead of local Whisper — see Tech Stack section above.

### sox not found
```bash
brew install sox
```

### Virtual env not activating
```bash
source .venv/bin/activate
# You should see (.venv) at the start of your terminal prompt
```

## License

MIT

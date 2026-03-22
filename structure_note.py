import os
import sys
from datetime import datetime
from anthropic import Anthropic
from config import ANTHROPIC_API_KEY


def structure_note(transcript: str, title: str = None) -> str:
    """
    Send transcript to Claude API and get back a clean structured Markdown note.

    Args:
        transcript: Raw transcript text from Whisper
        title: Optional title for the note

    Returns:
        Clean structured Markdown note as string
    """
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not set in .env file")

    if not transcript.strip():
        raise ValueError("Transcript is empty")

    client = Anthropic(api_key=ANTHROPIC_API_KEY)

    today = datetime.now().strftime("%Y-%m-%d %H:%M")

    print("🤖 Sending transcript to Claude...")

    prompt = f"""You are a smart note-taking assistant. 
I will give you a raw voice transcript and you will convert it into a clean, well-structured Markdown note.

Rules:
- Extract a concise title if none is provided
- Add a TL;DR summary at the top (2-3 sentences max)
- Organise content into logical sections with headings
- Extract any action items into a separate ## Action Items section
- Extract any decisions made into a ## Decisions section
- Keep the tone professional but natural
- Fix any transcription errors or repetitions
- Date: {today}

Raw transcript:
{transcript}

Return ONLY the Markdown note, nothing else. Start with the title as # Heading."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    structured_note = message.content[0].text
    print("✅ Note structured successfully!")
    return structured_note


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python structure_note.py <transcript_file>")
        print("Example: python structure_note.py transcript.txt")
        sys.exit(1)

    transcript_path = sys.argv[1]

    if not os.path.exists(transcript_path):
        print(f"❌ File not found: {transcript_path}")
        sys.exit(1)

    with open(transcript_path, "r") as f:
        transcript_text = f.read()

    try:
        result = structure_note(transcript_text)
        print("\n--- Structured Note ---")
        print(result)
        print("----------------------")
    except ValueError as e:
        print(f"❌ Config error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

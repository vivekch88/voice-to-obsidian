import os
import sys
import subprocess
import signal
from datetime import datetime
from pathlib import Path

from config import (
    OBSIDIAN_VAULT_PATH,
    NOTES_FOLDER,
    RECORDING_FILENAME,
    AUTO_GIT_COMMIT
)
from transcribe import transcribe_audio
from structure_note import structure_note


def create_note_filename(note_content: str) -> str:
    """Generate a filename from date and first line of note."""
    date_str = datetime.now().strftime("%Y-%m-%d-%H%M")
    first_line = note_content.split('\n')[0].replace('#', '').strip()
    first_line = "".join(c for c in first_line if c.isalnum() or c in (' ', '-', '_'))
    first_line = first_line[:50].strip().replace(' ', '-')
    return f"{date_str}-{first_line}.md"


def save_to_obsidian(note_content: str) -> str:
    """
    Save structured note to Obsidian vault.

    Args:
        note_content: Structured markdown note

    Returns:
        Path where note was saved
    """
    vault_path = Path(OBSIDIAN_VAULT_PATH)
    notes_path = vault_path / NOTES_FOLDER

    # Create folders if they don't exist
    notes_path.mkdir(parents=True, exist_ok=True)

    filename = create_note_filename(note_content)
    note_path = notes_path / filename

    with open(note_path, "w") as f:
        f.write(note_content)

    print(f"📝 Note saved to: {note_path}")
    return str(note_path)


def git_commit_note(note_path: str):
    """Auto commit the new note to git."""
    try:
        vault_path = Path(OBSIDIAN_VAULT_PATH)
        subprocess.run(
            ["git", "add", note_path],
            cwd=vault_path,
            check=True,
            capture_output=True
        )
        commit_msg = f"feat: add voice note {Path(note_path).name}"
        subprocess.run(
            ["git", "commit", "-m", commit_msg],
            cwd=vault_path,
            check=True,
            capture_output=True
        )
        print("✅ Note committed to Git!")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Git commit skipped: {e}")


def record_audio() -> str:
    """
    Record audio from microphone using sox.
    Press Ctrl+C to stop recording.

    Returns:
        Path to recorded audio file
    """
    print("\n🎙  Recording started — speak your thoughts!")
    print("⏹  Press Ctrl+C to stop recording\n")

    try:
        subprocess.run(
            [
                "sox", "-d",
                "-r", "16000",
                "-c", "1",
                "-b", "16",
                RECORDING_FILENAME
            ],
            check=True
        )
    except KeyboardInterrupt:
        print("\n⏹  Recording stopped!")
    except FileNotFoundError:
        print("❌ sox not found. Install with: brew install sox")
        sys.exit(1)

    return RECORDING_FILENAME


def run_pipeline():
    """Run the full voice to obsidian note pipeline."""
    print("=" * 50)
    print("🚀 Voice to Obsidian Note Pipeline")
    print("=" * 50)

    # Step 1 — Record
    audio_path = record_audio()

    if not os.path.exists(audio_path):
        print("❌ No audio file found. Did you speak before stopping?")
        sys.exit(1)

    # Step 2 — Transcribe
    try:
        transcript = transcribe_audio(audio_path)
    except Exception as e:
        print(f"❌ Transcription failed: {e}")
        sys.exit(1)

    if not transcript.strip():
        print("❌ Empty transcript — nothing to save")
        sys.exit(1)

    print(f"\n📄 Transcript:\n{transcript}\n")

    # Step 3 — Structure
    try:
        structured = structure_note(transcript)
    except Exception as e:
        print(f"❌ Structuring failed: {e}")
        sys.exit(1)

    print(f"\n📝 Structured Note:\n{structured}\n")

    # Step 4 — Save to Obsidian
    try:
        note_path = save_to_obsidian(structured)
    except Exception as e:
        print(f"❌ Failed to save note: {e}")
        sys.exit(1)

    # Step 5 — Git commit
    if AUTO_GIT_COMMIT:
        git_commit_note(note_path)

    print("\n" + "=" * 50)
    print("✅ Done! Note saved to Obsidian vault")
    print("=" * 50)


if __name__ == "__main__":
    run_pipeline()

#!/usr/bin/env python3
import json
import re
import sys
import subprocess
from pathlib import Path

STORE_DIR = Path.home() / ".claude" / "voice"
STORE_DIR.mkdir(parents=True, exist_ok=True)

def compact(text: str, limit: int = 120) -> str:
    text = re.sub(r"\s+", " ", (text or "").strip())
    return text if len(text) <= limit else text[: limit - 3] + "..."

def speak(text: str) -> None:
    text = compact(text, 160)
    if not text:
        return
    subprocess.Popen(["/usr/bin/say", text])  # macOS TTS

def task_file(session_id: str) -> Path:
    safe = re.sub(r"[^a-zA-Z0-9_-]+", "_", session_id or "unknown")
    return STORE_DIR / f"{safe}.txt"

def classify_label(prompt: str) -> str:
    p = (prompt or "").lower()
    if re.search(r"\b(test|pytest|unit test|npm test|pnpm test|yarn test)\b", p):
        return "tests"
    if re.search(r"\b(build|compile|bundle)\b", p):
        return "build"
    if re.search(r"\b(lint|eslint|ruff|flake8|format|prettier|gofmt)\b", p):
        return "lint/format"
    if re.search(r"\b(refactor)\b", p):
        return "refactor"
    if re.search(r"\b(debug|fix|bug)\b", p):
        return "fix"
    return ""

def main():
    raw = sys.stdin.read().strip()
    data = json.loads(raw or "{}")

    event = data.get("hook_event_name", "")
    session_id = data.get("session_id", "unknown")

    if event == "UserPromptSubmit":
        prompt = data.get("prompt", "")
        label = classify_label(prompt)
        spoken = label if label else compact(prompt, 90)
        task_file(session_id).write_text(spoken, encoding="utf-8")
        return

    if event == "Stop":
        speak("Task finished.")
        return

    if event == "Notification":
        ntype = data.get("notification_type") or data.get("notificationType") or ""
        message = data.get("message", "") or ""

        if ntype == "permission_prompt":
            speak("Claude needs your permission.")
        elif ntype == "idle_prompt":
            speak("Claude is waiting for your input.")
        elif ntype == "elicitation_dialog":
            speak("Claude needs some input to continue.")
        elif ntype == "auth_success":
            speak("Claude authenticated successfully.")
        else:
            speak(message if message else "Claude needs your attention.")
        return

if __name__ == "__main__":
    main()


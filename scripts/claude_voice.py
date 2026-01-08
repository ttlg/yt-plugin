#!/usr/bin/env python3
import json
import re
import sys
import subprocess

def compact(text: str, limit: int = 120) -> str:
    text = re.sub(r"\s+", " ", (text or "").strip())
    return text if len(text) <= limit else text[: limit - 3] + "..."

def speak(text: str) -> None:
    text = compact(text, 160)
    if not text:
        return
    subprocess.Popen(["/usr/bin/say", text])  # macOS TTS

def main():
    raw = sys.stdin.read().strip()
    data = json.loads(raw or "{}")

    event = data.get("hook_event_name", "")

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


#!/usr/bin/env python3
import json
import sys

def ring_bell():
    # Claude Code hookのstdoutが端末に出ないケースがあるので /dev/tty を叩く
    try:
        with open("/dev/tty", "w") as tty:
            tty.write("\a")  # BEL
            tty.flush()
    except Exception:
        pass

def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return

    # Notification Inputには notification_type が入る
    # 例: "permission_prompt" :contentReference[oaicite:7]{index=7}
    if data.get("notification_type") == "permission_prompt":
        ring_bell()

if __name__ == "__main__":
    main()


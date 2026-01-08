# claude-notifications

Voice notifications and terminal bell plugin for Claude Code.

## Features

| Event | Action |
|-------|--------|
| **Notification** | Voice + terminal bell for permission prompts |
| **Stop** | Says "Task finished" |

## Requirements

- macOS (uses `say` command)
- Python 3

## Installation

### 1. Add marketplace

```
/plugin marketplace add ttlg/yt-plugin
```

### 2. Install plugin

```
/plugin install claude-notifications@yt-market
```

### 3. Restart Claude Code

Restart Claude Code to load the plugin.

### 4. Verify installation

```
/plugin list
```

## Uninstall

```
/plugin uninstall claude-notifications@yt-market
```

## License

MIT

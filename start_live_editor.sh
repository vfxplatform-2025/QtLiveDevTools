#!/bin/bash
# Start Live UI Editor with rez environment
# Usage: ./start_live_editor.sh [ui_file] [port]

UI_FILE=${1:-"my_first_test.ui"}
PORT=${2:-7010}

echo "Starting Live UI Editor..."
echo "  UI File: $UI_FILE"
echo "  Port: $PORT"
echo ""

# Check if UI file exists
if [ ! -f "$UI_FILE" ]; then
    echo "Error: UI file not found: $UI_FILE"
    exit 1
fi

# Start Live Editor with rez environment
exec rez-env pyside6 -- python live_ui_editor.py --ui "$UI_FILE" --port "$PORT"

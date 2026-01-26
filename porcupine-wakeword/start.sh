#!/bin/sh
set -e

HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-10400}"
KEYWORDS="${KEYWORDS:-albert}"
ACCESS_KEY="${ACCESS_KEY}"
SENSITIVITY="${SENSITIVITY:-0.5}"
CUSTOM_MODEL_DIR="${CUSTOM_MODEL_DIR:-/app/models}"

# Check if access key is provided
if [ -z "$ACCESS_KEY" ]; then
    echo "ERROR: ACCESS_KEY environment variable is required!"
    echo "Get your free access key from: https://console.picovoice.ai/"
    exit 1
fi

# Build arguments
ARGS="--host ${HOST} --port ${PORT} --access-key ${ACCESS_KEY} --sensitivity ${SENSITIVITY}"

# Check if custom wake word files exist
CUSTOM_KEYWORD_PATHS=""
for keyword in $KEYWORDS; do
    KEYWORD_FILE="${CUSTOM_MODEL_DIR}/${keyword}.ppn"
    if [ -f "$KEYWORD_FILE" ]; then
        echo "Found custom wake word model: ${KEYWORD_FILE}"
        CUSTOM_KEYWORD_PATHS="${CUSTOM_KEYWORD_PATHS} ${KEYWORD_FILE}"
    fi
done

# Use custom keyword paths if available, otherwise use built-in keywords
if [ -n "$CUSTOM_KEYWORD_PATHS" ]; then
    ARGS="${ARGS} --keyword-paths${CUSTOM_KEYWORD_PATHS}"
    echo "Using custom wake word models"
else
    echo "No custom models found, trying built-in keywords"
    for keyword in $KEYWORDS; do
        ARGS="${ARGS} --keywords ${keyword}"
    done
fi

echo "Starting Porcupine wake word detection..."
echo "Wake words: ${KEYWORDS}"
echo "Sensitivity: ${SENSITIVITY}"
echo "Custom model directory: ${CUSTOM_MODEL_DIR}"

exec python /app/wyoming_porcupine.py $ARGS

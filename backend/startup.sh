#!/bin/bash
set -e

echo "============================================"
echo "  LAWAI Backend Starting..."
echo "============================================"

PORT="${PORT:-7860}"
echo "Starting gunicorn on port $PORT ..."
exec gunicorn \
    --workers 1 \
    --bind "0.0.0.0:${PORT}" \
    --timeout 300 \
    --keep-alive 5 \
    --preload \
    main:app

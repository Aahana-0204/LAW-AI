"""
Vercel Python serverless entry point.
Wraps the Flask app as a WSGI handler.
"""
import sys
import os

# Add backend root to path so `from app import create_app` works
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from main import app  # noqa: E402

# Vercel uses `app` or `handler` as the WSGI callable
handler = app

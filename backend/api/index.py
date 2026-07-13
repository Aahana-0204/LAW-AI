"""
Vercel Python serverless entry point.
Wraps the Flask app as a WSGI handler.
"""
import sys
import os
import traceback

# Add backend root to path so `from app import create_app` works
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

try:
    from main import app  # noqa: E402
    handler = app
except Exception as _boot_err:
    # Surface import errors as a plain WSGI response instead of FUNCTION_INVOCATION_FAILED
    _tb = traceback.format_exc()
    def handler(environ, start_response):
        body = f"BOOT ERROR:\n{_boot_err}\n\n{_tb}".encode()
        start_response("500 Internal Server Error", [
            ("Content-Type", "text/plain"),
            ("Content-Length", str(len(body))),
        ])
        return [body]

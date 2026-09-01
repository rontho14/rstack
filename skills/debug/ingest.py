#!/usr/bin/env python3
"""Tiny NDJSON ingest for browser debug probes. Port 8787."""
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import pathlib
from datetime import datetime, timezone
from urllib.parse import urlparse

DIR = pathlib.Path(".debug")
DIR.mkdir(exist_ok=True)
SESSIONS = {}


class H(BaseHTTPRequestHandler):
    def log_message(self, *_args):
        return

    def _read(self):
        n = int(self.headers.get("Content-Length", "0") or 0)
        raw = self.rfile.read(n) if n else b"{}"
        try:
            return json.loads(raw.decode() or "{}")
        except json.JSONDecodeError:
            return {}

    def _send(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()

    def do_GET(self):
        self._send(200, {"ok": True, "sessions": list(SESSIONS)})

    def do_POST(self):
        path = urlparse(self.path).path
        data = self._read()
        if path == "/session":
            name = (data.get("name") or "debug").replace("/", "-")[:40]
            sid = f"{name}-{datetime.now(timezone.utc).strftime('%H%M%S')}"
            log = DIR / f"debug-{sid}.log"
            log.touch()
            SESSIONS[sid] = log
            self._send(200, {"session_id": sid, "log_file": str(log)})
            return
        if path == "/log":
            sid = data.get("sessionId") or data.get("session_id")
            log = SESSIONS.get(sid) or DIR / f"debug-{sid}.log"
            data.setdefault("ts", datetime.now(timezone.utc).isoformat())
            with log.open("a") as f:
                f.write(json.dumps(data, default=str) + "\n")
            self._send(204, {})
            return
        self._send(404, {"error": "not found"})


if __name__ == "__main__":
    HTTPServer(("127.0.0.1", 8787), H).serve_forever()

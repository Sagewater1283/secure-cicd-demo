import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any


def build_response(path: str) -> tuple[int, dict[str, Any]]:
    if path == "/":
        return 200, {
            "message": "Secure CI/CD Demo API",
            "status": "running",
        }

    if path == "/health":
        return 200, {
            "status": "healthy",
        }

    if path == "/security-summary":
        return 200, {
            "pipeline_controls": [
                "Automated unit tests",
                "Static code linting",
                "Python dependency vulnerability scanning",
                "Static application security testing",
                "Container image scanning",
                "Least-privilege GitHub Actions permissions",
            ],
            "dependency_strategy": "Runtime uses Python standard library only to reduce supply-chain risk.",
            "bind_strategy": "The app defaults to localhost and requires explicit configuration to bind externally.",
        }

    return 404, {
        "error": "not_found",
    }


class SecureCICDRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        status_code, body = build_response(self.path)

        response = json.dumps(body).encode("utf-8")

        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)


def run_server() -> None:
    host = os.getenv("APP_HOST", "127.0.0.1")
    port = int(os.getenv("APP_PORT", "8000"))

    server = HTTPServer((host, port), SecureCICDRequestHandler)
    print(f"Secure CI/CD Demo API running on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()

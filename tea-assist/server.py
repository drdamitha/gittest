#!/usr/bin/env python3
"""TeaAssist full-stack chatbot app with built-in Python backend and modern UI."""

from __future__ import annotations

import json
import random
import re
from datetime import datetime
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"


class TeaAssistHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

    def do_POST(self):
        if self.path != "/api/chat":
            self.send_error(HTTPStatus.NOT_FOUND, "Endpoint not found")
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        payload = self.rfile.read(content_length) if content_length else b"{}"

        try:
            body = json.loads(payload.decode("utf-8"))
        except json.JSONDecodeError:
            self._send_json({"error": "Invalid JSON payload"}, HTTPStatus.BAD_REQUEST)
            return

        user_message = str(body.get("message", "")).strip()
        if not user_message:
            self._send_json({"error": "Message is required"}, HTTPStatus.BAD_REQUEST)
            return

        response = build_tea_response(user_message)
        self._send_json(response)

    def _send_json(self, data: dict, status: HTTPStatus = HTTPStatus.OK):
        encoded = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


def build_tea_response(message: str) -> dict:
    text = message.lower()
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    if any(k in text for k in ["fertilizer", "nutrient", "npk"]):
        reply = (
            "For tea, split fertilizer into 3 rounds: pre-monsoon, mid-monsoon, and post-monsoon. "
            "Use soil-test-based NPK ratios and add compost to improve moisture retention. "
            "If you share your soil pH and region, I can suggest a more precise schedule."
        )
        tips = ["Target soil pH around 4.5-5.5", "Apply fertilizer after light irrigation", "Avoid one-time heavy nitrogen"]
    elif any(k in text for k in ["disease", "blight", "pest", "aphid", "mite"]):
        reply = (
            "Start with field scouting every 3-4 days and remove infected leaves early. "
            "Use neem-based spray for mild pest pressure and rotate approved fungicides for severe infections."
        )
        tips = ["Check underside of leaves", "Spray in early morning/evening", "Maintain airflow through pruning"]
    elif any(k in text for k in ["weather", "rain", "forecast", "temperature"]):
        reply = (
            "For tea gardens, rainfall consistency matters more than heavy bursts. "
            "Mulch before dry spells and ensure drainage channels are clear before heavy rain."
        )
        tips = ["Monitor humidity daily", "Use shade nets during heat spikes", "Pause foliar sprays before rain"]
    elif any(k in text for k in ["market", "price", "sell", "auction"]):
        reply = (
            "Track weekly auction trends and keep quality lots separate for better pricing. "
            "Small-batch premium leaf often performs better with direct buyers than mixed lots."
        )
        tips = ["Log plucking date and grade", "Compare 4-week price averages", "Negotiate transport in advance"]
    else:
        reply = random.choice(
            [
                "I can help with fertilizer planning, pest alerts, weather actions, and market decisions for tea farms.",
                "Ask me about tea crop nutrition, disease prevention, irrigation timing, or leaf pricing strategies.",
            ]
        )
        tips = ["Try asking a specific farm question", "Include your location and season", "Share crop age for tailored advice"]

    suggestions = suggest_followups(text)
    return {"reply": reply, "tips": tips, "suggestions": suggestions, "timestamp": now}


def suggest_followups(text: str) -> list[str]:
    if re.search(r"fertilizer|nutrient|npk", text):
        return [
            "Create a month-wise fertilizer calendar",
            "How to correct low soil pH?",
            "Organic nutrient alternatives for tea",
        ]
    if re.search(r"disease|pest|blight|aphid|mite", text):
        return [
            "Symptoms to watch this week",
            "Safe spray rotation plan",
            "How to reduce fungal spread in humid fields",
        ]
    if re.search(r"weather|rain|temperature|forecast", text):
        return [
            "Pre-rain farm checklist",
            "Heatwave protection for young plants",
            "Drainage design tips for slopes",
        ]
    if re.search(r"market|price|auction|sell", text):
        return [
            "Best way to grade tea leaves",
            "How to negotiate with buyers",
            "Weekly market tracking template",
        ]
    return [
        "Give me a seasonal tea farming plan",
        "How to improve tea leaf quality",
        "Build a pest prevention checklist",
    ]


def run() -> None:
    server_address = ("0.0.0.0", 8000)
    httpd = ThreadingHTTPServer(server_address, TeaAssistHandler)
    print("TeaAssist running at http://localhost:8000")
    httpd.serve_forever()


if __name__ == "__main__":
    run()

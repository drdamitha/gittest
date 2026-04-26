# gittest

## TeaAssist full-stack chatbot

A tea farming assistant chatbot with a polished landing page UI and an integrated backend API.

### Features
- Modern tea-themed frontend with hero section and floating chat widget.
- End-to-end chat flow from browser to backend (`/api/chat`) and back.
- Context-aware responses for fertilizer, disease/pests, weather, and market topics.
- One-command startup using Python standard library only (no extra packages required).

### Run locally
```bash
cd tea-assist
python3 server.py
```

Then open: <http://localhost:8000>

### Project structure
- `tea-assist/server.py` – backend HTTP server + chat logic.
- `tea-assist/static/index.html` – landing page and chatbot layout.
- `tea-assist/static/styles.css` – responsive modern UI styling.
- `tea-assist/static/app.js` – frontend chat behavior and API integration.

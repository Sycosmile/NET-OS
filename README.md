# Net-OS 🌐

A lightweight autonomous network operating system simulation built with FastAPI. Features an AI-driven intelligence layer, health monitoring, adaptive behavior prediction, and a real-time dashboard.

[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-teal?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-ready-blue?style=flat-square&logo=docker)](https://docker.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

---

## Features

- **Autonomous Engine** — Self-managing core execution loop with scheduling
- **Intelligence Layer** — Health monitoring, behavior prediction, adaptive strategy
- **Memory Layer** — Persistent state management via SQLite
- **REST API** — FastAPI-powered endpoints for system control
- **Real-time Dashboard** — Lightweight HTML dashboard for system visibility
- **Docker Support** — Fully containerized with docker-compose

---

## Architecture

```
net-os/
├── app/
│   ├── main.py          # FastAPI entry point
│   ├── api.py           # API routes
│   └── config.py        # Configuration
├── core/
│   ├── engine.py        # Core execution engine
│   └── scheduler.py     # Task scheduling
├── intelligence/
│   ├── health.py        # System health monitoring
│   ├── predictor.py     # Behavior prediction
│   ├── strategy.py      # Adaptive strategy engine
│   └── behavior.py      # Behavioral analysis
├── memory/
│   └── db.py            # Persistent memory layer
├── router/
│   └── client.py        # Network routing client
├── workers/
│   └── daemon.py        # Background worker daemon
├── dashboard/
│   └── index.html       # Real-time web dashboard
├── Dockerfile
└── docker-compose.yml
```

---

## Setup

### Run locally

```bash
git clone https://github.com/Sycosmile/net-os.git
cd net-os
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

App runs at `http://localhost:8000`

### Run with Docker

```bash
docker-compose up --build
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | System status |
| GET | `/health` | Health check |
| GET | `/engine` | Engine status |

Full API docs available at `http://localhost:8000/docs` (Swagger UI)

---

## Author

**MR SYCO** — Cybersecurity student | Python developer | 3MTT Nigeria  
GitHub: [@Sycosmile](https://github.com/Sycosmile)

---

## License

MIT

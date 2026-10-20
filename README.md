# CYPHER Study Assistant

CYPHER is a browser-based AI study assistant with a FastAPI backend, Groq-powered responses, MongoDB-backed chat threads, a small JSON profile store, browser voice features, and a Three.js interface.

## Current status

This is an educational project and local prototype. It is not production-hardened: the API has no user authentication or rate limiting, thread routes are not scoped to an account, and the AI endpoint can incur provider usage. Add identity, authorization, abuse protection, and deployment monitoring before exposing it to untrusted users.

## Features

- Streaming study responses through FastAPI and LangChain's Groq integration.
- Thread creation, rename, history, and deletion backed by MongoDB.
- A local `memory.json` file for the assistant's profile and interaction context.
- Browser speech recognition and speech synthesis when supported by the browser.
- A responsive single-page interface with a Three.js background and temporary-chat mode.

## Technology

- Python 3.12+
- FastAPI and Uvicorn
- LangChain Core and `langchain-groq`
- MongoDB through Motor and PyMongo
- Vanilla HTML, CSS, JavaScript, and Three.js

## Prerequisites

- Python 3.12 or newer.
- A local MongoDB instance or a reachable MongoDB deployment.
- A Groq API key for model access.

## Local setup

```bash
git clone https://github.com/mahale800/study-bot-ai-assistant.git
cd study-bot-ai-assistant
python -m venv .venv
```

Activate the environment:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS or Linux
source .venv/bin/activate
```

Install dependencies and configure the environment:

```bash
python -m pip install -r requirements.txt
cp .env.example .env
```

On Windows, use `Copy-Item .env.example .env` instead of `cp`.

Set `GROQ_API_KEY` and, when MongoDB is not local, update `MONGO_URL`. `CORS_ORIGINS` can contain a comma-separated list of trusted browser origins; the default permits the local Uvicorn URLs only.

Start the backend:

```bash
python -m uvicorn main:app --reload
```

Open <http://127.0.0.1:8000> in a browser. The server serves `index.html` at the root route.

## Project structure

```text
agent.py          Groq and LangChain response logic
main.py           FastAPI routes and streaming endpoint
memory.py         MongoDB thread storage and JSON profile context
index.html        Frontend UI, voice controls, and Three.js scene
requirements.txt  Python dependencies
.env.example      Local configuration template
```

## Data and security notes

- Keep `.env` and `memory.json` local; never commit provider keys or private database URLs.
- The default MongoDB URL is `mongodb://localhost:27017`.
- The API currently has no authentication, authorization, rate limiting, or per-user data isolation.
- Restrict `CORS_ORIGINS` to known origins when serving the app outside local development.
- Treat the frontend as untrusted code and review any deployment that exposes the API to the public internet.

## Validation

There is currently no automated test suite. At minimum, parse the Python modules, start MongoDB, launch the API, and exercise chat, thread listing, rename, and deletion flows in a local environment.

## License

This project is licensed under the [MIT License](LICENSE).

## Author

Yash Mahale


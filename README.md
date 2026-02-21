# 💠 Study Bot (CYPHER AI Assistant)

<div align="center">
  <img src="https://img.shields.io/badge/Status-Production_Ready-00f3ff?style=for-the-badge&logo=rocket" alt="Status" />
  <img src="https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Groq-AI_Inference-f55036?style=for-the-badge&logo=ai" alt="Groq" />
  <img src="https://img.shields.io/badge/UI-WebGL_Three.js-black?style=for-the-badge&logo=three.js" alt="Three.js" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License" />
</div>

<br>

<div align="center">
  <strong>CYPHER is a cinematic, JARVIS-style AI study assistant featuring real-time voice synthesis, threaded memory persistence, and an interactive 3D WebGL interface.</strong>
  <br><br>
  <i>Alternative / Internal Title: Song Recommendation System</i>
</div>

---

## � System Preview

> **[UI Screenshot Placeholder]**  
> *(Insert a high-res screenshot of the glassmorphism UI with the 3D space background here)*

> **[Voice/Interaction Demo Placeholder]**  
> *(Insert a short GIF or video demonstrating speech recognition and the visual interface responding to voice)*

---

## 🔥 Features Overview

### 🎨 Cinematic UI/UX
- **Immersive 3D Parallax:** A responsive, interactive Three.js deep-space background.
- **Glassmorphism Design:** Premium frosted-glass panels, neon accents (`#00f3ff`), and dynamic typography.
- **Reactive System Vitals:** Live simulation of "Neural Load" and "Confidence" metrics that respond to the bot's processing state.
- **Intelligent Cursor:** A custom JARVIS-inspired magnetic cursor that changes color based on the AI's state (Thinking, Speaking, Listening).

### 🧠 High-Speed AI Processing
- **LangGraph & FastAPI:** Robust, asynchronous Python backend ensuring zero-blocking concurrent request handling.
- **Groq Inference Engine:** Delivers near-instantaneous LLM token streaming for true real-time conversation.
- **Context-Aware Tutor:** System prompts precisely tuned for academic assistance, concept breakdowns, and problem-solving without sycophantic filler.

### 🗣️ Seamless Voice System
- **Real-Time Speech-to-Text:** Continuous microphone listening using the native browser `SpeechRecognition` API.
- **Optimized Text-to-Speech (TTS):** Aggressive markdown and syntax cleaning ensures the browser's `speechSynthesis` engine reads responses naturally and cleanly.

### 💾 Persistent Threaded Memory
- **Local Storage:** Chats are saved to a local `memory.json` (acting as a lightweight NoSQL document store).
- **Session Management:** Maintain, rename, and purge multiple ongoing study sessions simultaneously.

### 🕶️ Incognito (Stealth) Mode
- **Zero-Trace Processing:** Pauses all memory recording for temporary questions.
- **Visual Shift:** The UI transitions from Cyan (`#00f3ff`) to a tactical Purple (`#a855f7`) to indicate the change in security posture.

---

## 🛠️ Tech Stack

### Frontend Architecture
- **Core:** HTML5, CSS3, Vanilla JavaScript (Zero bloated frameworks)
- **Graphics:** Three.js (WebGL rendering for background)

### Backend Architecture
- **Framework:** FastAPI (High-performance async Python framework)
- **Server:** Uvicorn (ASGI web server)

### AI & Data
- **Orchestration:** LangChain / LangGraph
- **LLM Provider:** Groq API (Llama-3 model series)
- **Storage:** File-based JSON (`memory.json`) for threaded persistence

---

## 📘 Academic Project Mapping

This repository serves as the official submission for the AI Study Assistant Chatbot requirement. Here is how the system directly satisfies the core criteria:

1. **Chatbot Requirement:** Handles complex, context-aware academic queries using LangGraph state management and high-speed LLM inference.
2. **Memory System:** Implements persistent, threaded conversations stored asynchronously in `memory.json`, allowing the bot to retain study context over long periods.
3. **API Backend:** Achieves strict frontend-backend separation using a RESTful Python FastAPI server.
4. **Real-World Application / Deployment Readiness:** A fully self-contained, production-ready system with proper environment segregation (ignoring `.env`) and aggressive frontend asset optimization.

---

## ⚙️ Quick Start Installation

**1. Clone the repository**
```bash
git clone https://github.com/mahale800/study-bot-ai-assistant.git
cd study-bot-ai-assistant
```

**2. Initialize Virtual Environment**
```bash
python -m venv .venv
# Activate on Windows:
.venv\Scripts\activate
# Activate on Mac/Linux:
source .venv/bin/activate
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure Environment**
Create a `.env` file in the root directory:
```env
GROQ_API_KEY="your_groq_api_key_here"
```

---

## 🚀 Usage

Start the production-ready FastAPI backend:
```bash
uvicorn main:app --reload
```

Then navigate your browser to the local interface:
```
http://127.0.0.1:8000
```

---

## � Project Structure

```text
study-bot-ai-assistant/
├── main.py             # FastAPI Server & Routes
├── agent.py            # LangGraph & Groq LLM Logic
├── memory.py           # Thread Persistence Logic
├── index.html          # Cinematic Frontend UI & Three.js Background
├── requirements.txt    # Python Dependencies
├── .env                # API Keys (Ignored by Git)
├── memory.json         # Chat History (Ignored by Git)
└── README.md           # Project Documentation
```

---

## 🔮 Future Scope

- **Vector Database Integration:** Migrating `memory.json` to a proper Vector DB (like Pinecone or Chroma) for semantic RAG operations over user study material (PDFs/Slides).
- **Multi-Modal Input:** Allowing users to upload images of equations or diagrams for the AI to analyze visually.
- **Cloud Deployment:** Containerization via Docker and deployment to AWS / Vercel.

---

## 📝 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">
  <i>Engineered with precision. Designed for the future.</i>
</div>

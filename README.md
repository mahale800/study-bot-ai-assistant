# CYPHER
**Cinematic AI Assistant with Voice, Memory, and Interactive UI**

CYPHER is a production-ready, JARVIS-inspired AI assistant featuring a fully cinematic 3D web interface, local memory persistence, voice recognition and synthesis, and deep neural analysis.

## 🚀 Features

- **Cinematic UI/UX:** Glassmorphism panels, interactive system vitals (CPU/Memory load simulation), and a deep 3D space parallax background (Three.js) that responds to cursor movement.
- **Voice System:** Seamless speech-to-text input with native browser `SpeechRecognition` and deeply integrated `speechSynthesis` (TTS) that cleans markdown/symbols for natural pronunciation.
- **AI Processing:** Uses LangGraph and FastAPI to route inputs through Groq's high-speed inference.
- **Persistent Memory:** Local JSON-based thread storage allows you to maintain multiple ongoing conversations, easily renamed or purged.
- **Reactive Modes:** The cursor and HUD update dynamically to reflect the AI's internal state (Thinking, Speaking, Listening, Idle, Incognito).
- **Temp / Incognito Mode:** Stealth communication that bypasses memory storage, changing the interface aesthetic to a purple tactical theme.

## 🛠️ Tech Stack

- **Frontend:** HTML5, CSS3, Vanilla JavaScript, Three.js (WebGL)
- **Backend:** Python, FastAPI, Uvicorn
- **AI / LLM:** LangChain, LangGraph, Groq API
- **Local Storage:** File-based JSON (`memory.json`)

## ⚙️ Setup Instructions

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/cypher.git
cd cypher
```

**2. Create a Virtual Environment**
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

**4. Set Environment Variables**
Create a `.env` file in the root directory and add your Groq API key:
```env
GROQ_API_KEY="your_groq_api_key_here"
```

## 🚀 Running the System

Start the FastAPI backend server:
```bash
uvicorn main:app --reload
```

Then, open your browser and navigate to:
```
http://127.0.0.1:8000
```

## 🔒 Security Note
- Never commit your `.env` file or `memory.json`.
- These are excluded in the `.gitignore` by default.

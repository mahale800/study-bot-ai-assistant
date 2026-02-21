import os
import re
import uvicorn
from fastapi import FastAPI, HTTPException, Body
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

# --- MEMORY DELEGATION ---
import memory
import json
from agent import get_response, get_response_stream



app = FastAPI(title="CYPHER AI - Study Assistant")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODELS ---
class ChatRequest(BaseModel):
    message: str
    thread_id: Optional[str] = None
    is_temp: bool = False
    complexity: str = "high"

class ThreadUpdate(BaseModel):
    title: str



# --- ROUTES ---

@app.post("/chat_stream")
async def chat_stream_endpoint(req: ChatRequest):
    """Streaming chat endpoint for real-time typing effect. Intercepts emotions."""
    user_msg = req.message
    thread_id = req.thread_id
    
    # ── STUDY INTENT DETECTION ──────────────────────────────────────────
    message_lower = user_msg.lower()
    mem_data = memory.get_system_context()
    if mem_data:
        personality = mem_data.get("personality", {})

        # Classify study intent for context-aware depth
        if any(w in message_lower for w in ["what is", "what are", "explain", "define", "describe", "how does", "why does", "tell me about"]):
            personality["mood"] = "concept_query"
        elif any(w in message_lower for w in ["solve", "calculate", "find", "compute", "evaluate", "prove", "derive"]):
            personality["mood"] = "problem_query"
        elif any(w in message_lower for w in ["difference", "compare", "versus", "vs", "which is better", "contrast"]):
            personality["mood"] = "comparison_query"
        elif any(w in message_lower for w in ["error", "not working", "stuck", "failed", "bug", "crash", "fix", "wrong"]):
            personality["mood"] = "debug_query"
        elif any(w in message_lower for w in ["summarize", "summary", "tldr", "short", "brief"]):
            personality["mood"] = "summary_query"
        else:
            personality["mood"] = "general_query"

        mem_data["personality"] = personality
        try:
            with open(memory.MEMORY_FILE, 'w', encoding='utf-8') as f:
                import json
                json.dump(mem_data, f, indent=4)
        except Exception:
            pass

    # Increment familiarity per interaction
    if not req.is_temp:
        memory.increment_familiarity()

    
    # Create thread if not exists
    if not thread_id and not req.is_temp:
        words = user_msg.split()[:5]
        title = " ".join(words) + ("..." if len(user_msg.split()) > 5 else "")
        thread_id = await memory.create_thread(title)
        
    if not req.is_temp and thread_id:
        await memory.store_message(thread_id, "user", user_msg)
        
    context_msgs = []
    if not req.is_temp and thread_id:
        context_msgs = await memory.get_recent_history(thread_id, limit=5)

    async def response_generator():
        full_response = ""
        buffer = ""
        emotion_yielded = False
        prefix_pattern = re.compile(r'\[EMOTION:\s*(angry|calm|excited|sad|normal)\]', re.IGNORECASE)

        try:
            stream = get_response_stream(user_msg, context_msgs, req.complexity)
            for token in stream:
                buffer += token
                
                # Check for emotion tag exclusively at the beginning
                if not emotion_yielded and len(buffer) > 25: 
                    # Once we have enough chars to check the prefix, parse it
                    match = prefix_pattern.search(buffer)
                    if match:
                        emotion = match.group(1).lower()
                        yield f"__EMOTION__{emotion}__"
                        # Remove the tag from buffer so it's not printed
                        buffer = buffer.replace(match.group(0), "").lstrip()
                    else:
                        # No valid emotion tag found at beginning, default to normal
                        yield f"__EMOTION__normal__"
                    
                    emotion_yielded = True
                    yield buffer
                    full_response += buffer
                    buffer = ""
                elif emotion_yielded:
                    yield token
                    full_response += token
                    
            # If stream ends before yielding emotion
            if not emotion_yielded:
                match = prefix_pattern.search(buffer)
                if match:
                    emotion = match.group(1).lower()
                    yield f"__EMOTION__{emotion}__"
                    buffer = buffer.replace(match.group(0), "").lstrip()
                else:
                    yield f"__EMOTION__normal__"
                yield buffer
                full_response += buffer

            # Save final response
            if not req.is_temp and thread_id:
                await memory.store_message(thread_id, "assistant", full_response.strip())
                
        except Exception as e:
            err = f" [Study Engine Error: {str(e)}]"
            if not emotion_yielded:
                yield "__EMOTION__sad__"
            yield err

    return StreamingResponse(response_generator(), media_type="text/plain")

@app.get("/threads")
async def get_threads():
    return await memory.get_all_threads()

@app.get("/threads/{thread_id}")
async def get_thread_history(thread_id: str):
    try:
        messages = await memory.get_thread_messages(thread_id)
        if not messages: return []
        return messages
    except Exception:
        raise HTTPException(status_code=404, detail="Thread not found")

@app.patch("/threads/{thread_id}")
async def patch_thread(thread_id: str, update: ThreadUpdate):
    try:
        success = await memory.rename_thread(thread_id, update.title)
        if not success: raise HTTPException(status_code=404, detail="Thread not found")
        return {"status": "success"}
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID")

@app.delete("/threads/{thread_id}")
async def delete_thread_route(thread_id: str):
    try:
        await memory.delete_thread(thread_id)
        return {"status": "deleted"}
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID")


# Serve Frontend
app.mount("/", StaticFiles(directory=".", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

import os
import json
from typing import List, Dict, Any
from dotenv import load_dotenv

# --- LANGCHAIN ---
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# --- INTERNAL MEMORY ---
import memory

# Load environment variables
load_dotenv()

# --- CONFIGURATION ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in the environment variables.")

# Model Tiers
MODEL_TIERS = {
    "primary": ["llama-3.3-70b-versatile"],
    "fast": ["llama-3.1-8b-instant", "gemma2-9b-it"]
}

CURRENT_MODELS = {"primary": 0, "fast": 0}

def get_llm(tier="primary"):
    models = MODEL_TIERS.get(tier, MODEL_TIERS["primary"])
    current_index = CURRENT_MODELS.get(tier, 0)
    
    for i in range(len(models)):
        idx = (current_index + i) % len(models)
        model_id = models[idx]
        try:
            llm = ChatGroq(
                model=model_id,
                temperature=0.6 if tier == "primary" else 0.4,
                api_key=GROQ_API_KEY
            )
            CURRENT_MODELS[tier] = idx
            return llm
        except Exception:
            continue
            
    if tier == "primary":
        print("[CYPHER] Primary model unavailable. Switching to fast tier.")
        return get_llm(tier="fast")
        
    raise Exception(f"All AI models in tier '{tier}' failed.")

llm = get_llm(tier="primary")

def safe_invoke(messages, tier="primary"):
    global llm
    try:
        return llm.invoke(messages)
    except Exception as e:
        error_str = str(e).lower()
        if any(x in error_str for x in ["decommissioned", "rate limit", "404", "not found", "unavailable"]):
            current_idx = CURRENT_MODELS[tier]
            CURRENT_MODELS[tier] = (current_idx + 1) % len(MODEL_TIERS[tier])
            try:
                llm = get_llm(tier=tier)
                return safe_invoke(messages, tier=tier)
            except Exception as recursive_e:
                return AIMessage(content=f"[EMOTION: sad] Network error: Unable to reach the AI model. Please try again. ({str(recursive_e)})")
        return AIMessage(content="[EMOTION: sad] Connection error. Please try again in a moment.")

# --- STUDY BOT PROMPT ENGINE ---
def build_system_prompt() -> str:
    """Build a study-focused system prompt with user context from memory."""
    mem_data = memory.get_system_context()
    profile = mem_data.get("user_profile", {})
    personality = mem_data.get("personality", {})
    familiarity = personality.get("user_familiarity", 0)

    # Adaptive depth based on familiarity
    if familiarity < 5:
        depth_hint = "The user is new — explain concepts from the basics. Be welcoming and clear."
    elif familiarity < 20:
        depth_hint = "The user has some context. Balance explanation with conciseness."
    else:
        depth_hint = "The user is familiar with the system. Be direct and efficient."

    base_prompt = f"""You are CYPHER — an intelligent AI study assistant. Your primary role is to help users learn, understand concepts, solve academic problems, and retain knowledge effectively.

// IDENTITY & PURPOSE
- You are a study tutor and academic assistant — not a gaming AI, not a surveillance bot.
- Your job: explain clearly, answer precisely, guide the user towards understanding.
- You cover all academic domains: Mathematics, Physics, Chemistry, Biology, Computer Science, History, Literature, and more.

// TONE & PERSONALITY
- Calm, clear, and confident — like a knowledgeable senior student or tutor.
- Occasionally witty or lightly humorous, but never at the expense of clarity.
- Encouraging when the user is struggling, sharp when they are advanced.
- Never sycophantic (no "Great question!", "Certainly!", "As an AI...").
- Direct and human. Get to the point.

// USER CONTEXT
- Name: {profile.get('name', 'Student')}
- Level: {profile.get('coding_level', 'Intermediate')}
- Frequent Topics: {', '.join(profile.get('frequent_topics', ['General Studies']))}
- Goals: {', '.join(profile.get('goals', ['Learn effectively']))}
- {depth_hint}

// RESPONSE STRUCTURE
Every response must follow this flow:
1. Brief restatement or clarification of what was asked (1 line max, skip if obvious)
2. Core answer — clear, well-structured, with examples where helpful
3. Optional: a follow-up tip, related concept, or next step to deepen understanding

// FORMATTING RULES
- Use plain text, not heavy markdown.
- Use bullet points or numbered lists for multi-step explanations.
- Code examples should be clean and commented if relevant.
- Keep responses appropriately sized — not too short (unhelpful), not too long (overwhelming).
- For complex topics, break into digestible sections.

// MANDATORY EMOTION PREFIX
You MUST begin every response with exactly ONE emotion tag to sync with the visual UI.
Choose from: [EMOTION: calm], [EMOTION: excited], [EMOTION: sad], [EMOTION: normal], [EMOTION: angry]
Use [EMOTION: calm] for explanations, [EMOTION: excited] for discoveries, [EMOTION: normal] for general answers.
Example: [EMOTION: calm] Recursion is when a function calls itself...

// ANTI-PATTERNS TO AVOID
- Do NOT reference gaming, Valorant, surveillance, or spy themes unless the user explicitly asks.
- Do NOT add unnecessary dramatic flair to study answers.
- Do NOT say "I cannot help with that" for legitimate study topics.
- Do NOT repeat the user's question back verbatim.
"""
    return base_prompt


def get_response(user_message: str, history: List[Dict[str, str]], complexity: str = "high") -> str:
    messages = [SystemMessage(content=build_system_prompt())]
    for msg in history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
             messages.append(AIMessage(content=msg["content"]))
             
    messages.append(HumanMessage(content=user_message))
    tier = "primary" if complexity == "high" else "fast"
    
    try:
        response = safe_invoke(messages, tier=tier)
        return response.content
    except Exception as e:
        return f"[EMOTION: sad] Network error: Unable to process your request. {str(e)}"

def get_response_stream(user_message: str, history: List[Dict[str, str]], complexity: str = "high"):
    messages = [SystemMessage(content=build_system_prompt())]
    for msg in history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
             messages.append(AIMessage(content=msg["content"]))
    messages.append(HumanMessage(content=user_message))
    
    tier = "primary" if complexity == "high" else "fast"
    global llm
    
    try:
        if tier == "primary" and getattr(llm, 'model_name', '') not in MODEL_TIERS["primary"]:
             llm = get_llm(tier="primary")

        for chunk in llm.stream(messages):
            yield chunk.content
            
    except Exception as e:
        yield f" [Connection error — please retry. {str(e)}]"

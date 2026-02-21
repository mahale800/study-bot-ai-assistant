import os
import json
from datetime import datetime
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

# --- MONGO DB SETUP ---
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URL)
db = client.cypher_ai

# Fix ObjectId serialization
def serialize_doc(doc):
    if not doc: return None
    doc["_id"] = str(doc["_id"])
    return doc

# --- MEMORY JSON ---
MEMORY_FILE = "memory.json"

DEFAULT_MEMORY = {
    "user_profile": {
        "name": "Student",
        "profession": "Student",
        "goals": ["Learn effectively", "Understand concepts deeply", "Excel academically"],
        "coding_level": "Intermediate",
        "frequent_topics": ["Mathematics", "Computer Science", "Physics"],
        "preferences": ["Clear explanations", "Examples", "Step-by-step breakdown"],
        "behavior_patterns": [],
        "repeated_mistakes": []
    },
    "personality": {
        "tone": "helpful-intelligent",
        "mood": "neutral",
        "user_familiarity": 0,
        "trust_level": 0
    }
}

def _ensure_memory_file():
    if not os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_MEMORY, f, indent=4)

def get_system_context():
    """Reads memory.json to inject long-term profile and personality data."""
    _ensure_memory_file()
    try:
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except Exception:
        return DEFAULT_MEMORY

def increment_familiarity():
    """Increase familiarity score slowly as interactions happen."""
    _ensure_memory_file()
    try:
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        data.setdefault("personality", {})
        fam = data["personality"].get("user_familiarity", 0)
        data["personality"]["user_familiarity"] = fam + 1
        
        with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Memory update error: {e}")

# --- DB OPERATIONS ---
async def create_thread(title: str):
    new_thread = await db.chats.insert_one({
        "title": title,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    })
    return str(new_thread.inserted_id)

async def store_message(thread_id: str, role: str, content: str):
    await db.messages.insert_one({
        "thread_id": thread_id,
        "role": role,
        "content": content,
        "timestamp": datetime.utcnow()
    })
    await db.chats.update_one(
        {"_id": ObjectId(thread_id)},
        {"$set": {"updated_at": datetime.utcnow()}}
    )

async def get_recent_history(thread_id: str, limit: int = 10):
    cursor = db.messages.find({"thread_id": thread_id}).sort("timestamp", -1).limit(limit)
    history = await cursor.to_list(length=limit)
    return [{"role": m["role"], "content": m["content"]} for m in reversed(history)]

async def get_all_threads():
    cursor = db.chats.find({}).sort("updated_at", -1)
    threads = await cursor.to_list(length=100)
    return [serialize_doc(t) for t in threads]

async def get_thread_messages(thread_id: str):
    cursor = db.messages.find({"thread_id": thread_id}).sort("timestamp", 1)
    messages = await cursor.to_list(length=1000)
    return [serialize_doc(m) for m in messages]

async def rename_thread(thread_id: str, new_title: str):
    result = await db.chats.update_one(
        {"_id": ObjectId(thread_id)},
        {"$set": {"title": new_title, "updated_at": datetime.utcnow()}}
    )
    return result.modified_count > 0

async def delete_thread(thread_id: str):
    await db.chats.delete_one({"_id": ObjectId(thread_id)})
    await db.messages.delete_many({"thread_id": thread_id})
    return True

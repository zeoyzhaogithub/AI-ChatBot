from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

def connect_mongodb():
    client = MongoClient(os.getenv("MONGODB_URI"))
    db = client["chatbot_db"]
    return db.chat_sessions

def save_conversation(session_id, user_id, messages):
    collection = connect_mongodb()
    doc = {
        "session_id": session_id,
        "user_id": user_id,
        "timestamp": datetime.utcnow(),
        "messages": messages
    }
    collection.insert_one(doc)
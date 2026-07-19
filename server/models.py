from datetime import datetime

class ResponseModel:
    def __init__(self, db):
        self.collection = db['responses'] if db is not None else None

    def find_response(self, intent, emotion=None):
        if self.collection is None:
            return None
        query = {"intent": intent}
        if emotion:
            query["emotion"] = emotion
        return self.collection.find_one(query)

    def add_response(self, intent, text, emotion=None, metadata=None):
        if self.collection is None:
            return None
        doc = {
            "intent": intent,
            "text": text,
            "emotion": emotion,
            "created_at": datetime.utcnow(),
            "metadata": metadata or {}
        }
        return self.collection.insert_one(doc)

class ChatLogModel:
    def __init__(self, db):
        if db is not None:
            self.collection = db['chat_logs']
            # Ensure TTL index for auto-deletion (e.g., 24 hours)
            self.collection.create_index("created_at", expireAfterSeconds=86400)
        else:
            self.collection = None

    def log_message(self, room_id, user_id, message, role='user', emotion=None):
        if self.collection is None:
            return None
        doc = {
            "room_id": room_id,
            "user_id": user_id,
            "role": role, # 'user' or 'assistant'
            "message": message,
            "emotion": emotion,
            "created_at": datetime.utcnow()
        }
        return self.collection.insert_one(doc)

    def get_recent_history(self, room_id, limit=10):
        if self.collection is None:
            return []
        
        # Find messages for this room, sorted by time
        cursor = self.collection.find({"room_id": room_id}).sort("created_at", -1).limit(limit)
        
        history = []
        for doc in cursor:
            history.append({
                "role": doc.get("role", "user"),
                "content": doc.get("message", "")
            })
        
        # Return in chronological order
        return history[::-1]

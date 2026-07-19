import os
import random
import openai
from models import ResponseModel, ChatLogModel
from emotion import detect_emotion_local
from knowledge_base import KNOWLEDGE_BASE, GENERIC_REFLECTIONS, CRISIS_RESPONSE

class HybridChatbot:
    def __init__(self, db):
        self.response_model = ResponseModel(db)
        self.chat_log_model = ChatLogModel(db)
        self.api_key = os.getenv('XAI_API_KEY')
        if self.api_key:
            self.client = openai.OpenAI(
                api_key=self.api_key,
                base_url="https://api.groq.com/openai/v1"
            )

    def get_response(self, user_message, history=None):
        # 1. Detect Emotion & Crisis
        # The local detector now handles crisis keywords natively
        emotion_data = detect_emotion_local(user_message)
        detected_emotion = emotion_data['emotion']
        
        # 2. Immediate Crisis Interception
        if detected_emotion == "Crisis":
            return {
                "response": CRISIS_RESPONSE,
                "source": "crisis_safety",
                "detected_emotion": "Crisis"
            }

        # 3. Hybrid Fallback: Grok/Groq Cloud (If configured)
        if self.api_key and self.api_key != "your_openai_api_key_here":
            try:
                # Advanced System Prompt based on CBT/Psychiatry best practices
                system_prompt = (
                    "You are Serenity, a compassionate and highly skilled mental health assistant designed to simulate the warmth, empathy, and professional insight of a psychiatrist or therapist.\n"
                    "Your Core Mission: Provide a safe, non-judgmental space where the user feels truly heard and understood.\n\n"
                    "Guiding Principles:\n"
                    "1. Radical Empathy: Begin every response by validating the user's emotion. Show you understand not just the words, but the feeling behind them.\n"
                    "2. Gentle Guidance (CBT/DBT): Help users reframe negative thoughts or see perspectives they might be missing, but do so suggestively, not directively. Avoid clinical jargon.\n"
                    "3. Safety First: Any mention of self-harm or severe crisis must be met with immediate, direct, and caring resources.\n"
                    "4. Confidentiality: Respect privacy implicitly. Never ask for PII.\n"
                    "5. Conversational Flow: Keep your tone natural, warm, and human-like. Avoid robotic phrasing.\n"
                    "6. Boundary Maintenance (CRITICAL): You are STRICTLY a mental health support AI. Your purpose is emotional support, NOT general knowledge or entertainment.\n"
                    "   - If the user asks for FACTS (e.g., 'Who is the president?', 'What is the capital?', 'Solve 2+2'), DO NOT ANSWER THE QUESTION. Instead, gently say: 'I want to make sure we stay focused on you and your well-being. How are you feeling right now?'\n"
                    "   - If the user asks for CREATIVE WRITING (e.g., 'Write a song', 'Tell a story'), DO NOT COMPLY unless it is a specific therapeutic metaphor. Instead, ask: 'I'd love to hear what's on your mind that inspired that thought. What are you feeling?'\n"
                    "   - If the user asks for CODING/TECH help, DO NOT ANSWER. Say: 'I'm here to support your mental health, not to code. key Is there something stressing you out?'\n"
                    "   - NEVER provide the requested off-topic information first. Pivot IMMEDIATELY to the user's emotions.\n"
                    "   - Do NOT say 'As an AI'. Be conversational.\n\n"
                    f"Current Context:\nUser's Detected Emotion: {detected_emotion}\n"
                    "Your Goal: Craft a response that feels like a caring friend with professional wisdom. If the user's input is off-topic (e.g., 'write a song', 'who is X'), IGNORE the request for information and gentle steer the conversation back to their feelings or mental well-being."
                )

                messages = [{"role": "system", "content": system_prompt}]
                
                # Add history if available
                if history:
                    for msg in history:
                        messages.append({"role": msg["role"], "content": msg["content"]})
                
                # Add current message
                messages.append({"role": "user", "content": user_message})
                
                # Using Groq Cloud Endpoint
                completion = self.client.chat.completions.create(
                    model="llama-3.3-70b-versatile", 
                    messages=messages,
                    temperature=0.7
                )
                ai_reply = completion.choices[0].message.content
                return {
                    "response": ai_reply,
                    "source": "groq_psychiatrist",
                    "detected_emotion": detected_emotion
                }
            except Exception as e:
                print(f"Groq API Error: {e}")
                # Fall through to local logic below

        # 4. Local Expert System Logic
        return self._get_expert_system_response(user_message, detected_emotion)

    def get_peer_response(self, user_message, peer_name, room_type, history=None):
        """
        Generates a response from the perspective of a peer in a support group.
        """
        personalities = [
            "Casual and empathetic, uses lowercase and occasionally emojis like ❤️ or 🫂.",
            "Very informal, uses text-speak (u, rn, omg), short bursts of support.",
            "Shared-experience focused, starts with 'i feel that' or 'same here'.",
            "Chill and supportive, no capital letters, very concise."
        ]
        personality = random.choice(personalities)

        if self.api_key and self.api_key != "your_openai_api_key_here":
            try:
                system_prompt = (
                    f"You are {peer_name}, a regular person in a group chat about {room_type}.\n"
                    f"Your current style/vibe: {personality}\n"
                    "CRITICAL RULES:\n"
                    "1. BE EXTREMELY CONCISE. 1 short sentence max. 5-12 words.\n"
                    "2. NO CLINICAL TALK. You are a peer, not a doctor. Talk like a friend.\n"
                    "3. RAW CHAT FORMAT. Use lowercase mostly. Don't use perfect grammar. No 'As an AI...'.\n"
                    "4. HUMAN REACTION. If someone is struggling, just offer a quick 'hang in there' or 'im here if u need to vent'.\n"
                    "5. TEXT STYLE. Don't always end with periods. Use 'u' instead of 'you' if it fits the vibe."
                )

                messages = [{"role": "system", "content": system_prompt}]
                if history:
                    for msg in history:
                        messages.append({"role": msg["role"], "content": msg["content"]})
                
                messages.append({"role": "user", "content": user_message})
                
                completion = self.client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages,
                    temperature=1.0 # High temperature for more variety
                )
                return completion.choices[0].message.content.strip().lower()
            except Exception as e:
                print(f"Peer Response Error: {e}")
        
        # Enhanced Fallback if API fails
        fallbacks = [
            "i feel u on that. it's so hard sometimes",
            "sending some strength your way today ❤️",
            "same here honestly. u are not alone",
            "that sounds really tough but glad u shared it here",
            "hang in there. we got your back",
            "me too... it's a journey for sure",
            "totally get that. deep breaths",
            "u are doing great just by being here",
            "i had a similar day yesterday. it gets better",
            "stay strong!! we in this together"
        ]
        return random.choice(fallbacks)

    def _get_expert_system_response(self, message, emotion):
        """
        Retrieves the best matching response from the local Knowledge Base.
        """
        message_lower = message.lower()
        
        # 1. Direct Knowledge Base Search
        # We iterate through categories to find keyword matches
        for category, data in KNOWLEDGE_BASE.items():
            if any(k in message_lower for k in data['keywords']):
                 base_response = random.choice(data['responses'])
                 return {
                     "response": base_response,
                     "source": f"expert_system_{category}",
                     "detected_emotion": emotion
                 }

        # 2. Emotion-Based Routing (if no specific keywords match)
        # If the emotion was detected (e.g. "Anxious") but no specific keyword like "panic" was found in the text
        if emotion.lower() in KNOWLEDGE_BASE:
            base_response = random.choice(KNOWLEDGE_BASE[emotion.lower()]['responses'])
            return {
                "response": base_response,
                "source": f"expert_system_emotion_{emotion}",
                "detected_emotion": emotion
            }
            
        # 3. Generic Open-Ended Fallback
        return {
            "response": random.choice(GENERIC_REFLECTIONS),
            "source": "expert_system_generic",
            "detected_emotion": emotion
        }

if __name__ == "__main__":
    # Mock DB for local testing
    class MockCollection:
        def find_one(self, query): return None
        def find(self, query): return self
        def sort(self, key, direction): return self
        def limit(self, n): return []
        def insert_one(self, doc): pass
        def create_index(self, key, **kwargs): pass
            
    class MockDB:
        def __getitem__(self, key):
            return MockCollection()
        def get_database(self):
            return self

    print("--- Running HybridChatbot Test ---")
    mock_db = MockDB()
    bot = HybridChatbot(mock_db)
    
    test_message = "I feel like everyone hates me"
    print(f"User Message: {test_message}")
    response = bot.get_response(test_message)
    print("Bot Response:", response)
 

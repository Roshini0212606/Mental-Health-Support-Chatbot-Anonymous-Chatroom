from textblob import TextBlob
import os

def detect_emotion_local(text):
    """
    Enhanced local sentiment analysis using TextBlob and keyword heuristics.
    Returns a dictionary with polarity, subjectivity, and a mapped emotion.
    """
    text_lower = text.lower()
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    
    # 1. Crisis / Safety High Priority
    crisis_keywords = [
        "suicidal", "suicide", "kill myself", "end it all", "hurt myself", 
        "die", "death", "overdose", "cutting", "don't want to live"
    ]
    if any(word in text_lower for word in crisis_keywords):
        return {
            "emotion": "Crisis",
            "polarity": -1.0,
            "subjectivity": 1.0
        }

    # 2. Nuanced Keyword Mapping (overrides simple polarity)
    if any(w in text_lower for w in ["anxious", "anxiety", "panic", "nervous", "scared", "fear", "worried"]):
        emotion = "Anxious"
    elif any(w in text_lower for w in ["lonely", "alone", "isolated", "nobody", "miss people"]):
        emotion = "Lonely"
    elif any(w in text_lower for w in ["thank", "thanks", "appreciate", "grateful", "good bot"]):
        emotion = "Gratitude"
    elif any(w in text_lower for w in ["tired", "exhausted", "sleep", "insomnia", "awake"]):
        emotion = "Tired"
    elif polarity > 0.4:
        emotion = "Happy"
    elif polarity < -0.3:
        emotion = "Sad"
    elif polarity < -0.1:
        emotion = "Frustrated"
    else:
        emotion = "Neutral"
        
    return {
        "emotion": emotion,
        "polarity": polarity,
        "subjectivity": blob.sentiment.subjectivity
    }

def detect_emotion_openai(text, client):
    """
    Uses OpenAI to strictly classify emotion into categories if available.
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Classify the user's emotion into one of these: Happy, Sad, Anxious, Angry, Lonely, Crisis, Neutral, Gratitude, Tired. Return ONLY the one word label."},
                {"role": "user", "content": text}
            ],
            temperature=0
        )
        return completion.choices[0].message.content.strip()
    except:
        return None



"""
Mental Health Knowledge Base & Pre-defined Responses.
Simulates a retrieved dataset from "Mental Health Counseling Conversations".
"""

KNOWLEDGE_BASE = {
    "grief": {
        "keywords": ["lost", "died", "passed away", "gone", "grief", "missing him", "missing her", "death", "funeral"],
        "responses": [
            "I am so deeply sorry for your loss. Grief is a unique and personal journey that comes in waves. How have you been holding up today?",
            "Losing someone is one of the hardest things we go through. It's meaningful to honor your feelings, whether they are sadness, anger, or numbness. Would you like to share a memory of them?",
            "Please be gentle with yourself. There is no timeline for grief. It takes as long as it takes. I'm here to listen to whatever you need to say about them.",
            "I hear the pain in your words. It is a testament to how much they meant to you. How can I support you in this moment?"
        ]
    },
    "anxiety": {
        "keywords": ["anxious", "nervous", "scared", "worried", "panic", "fear", "dread", "tense", "heart racing", "overthinking"],
        "responses": [
            "I hear you. Anxiety can feel like a storm inside. Let's try to ground ourselves. Can you tell me 3 things you see around you right now?",
            "That sounds incredibly draining. Anxiety often tries to predict the future. Let's come back to the present. You are safe here with me.",
            "It's okay to feel scared. Your feelings are valid, but they are not facts. What is the specific thought that is worrying you the most?",
            "Take a slow, deep breath. In... and out. You've gotten through difficult moments before, and we will get through this one too."
        ]
    },
    "depression": {
        "keywords": ["sad", "depressed", "hopeless", "tired", "empty", "cry", "crying", "unhappy", "pain", "darkness", "heavy"],
        "responses": [
            "I appreciate you sharing that with me. It takes courage to speak about these heavy feelings. You are not a burden, and you don't have to carry this alone.",
            "Depression can lie and tell us we'll feel this way forever, but feelings are temporary. Even if it feels impossible, I'm proud of you for reaching out today.",
            "It sounds like you're carrying a very heavy weight. I'm here to sit in the dark with you for as long as you need. You matters.",
            "I'm listening. Sometimes the smallest step, like drinking a glass of water, is a victory. Have you been able to be kind to yourself at all today?"
        ]
    },
    "loneliness": {
        "keywords": ["lonely", "alone", "nobody", "friendless", "isolated", "rejected", "outcast"],
        "responses": [
            "Loneliness is a deeply human feeling, but it doesn't mean you are unworthy of connection. I am here connecting with you right now.",
            "It sounds painful to feel so isolated. Connection starts with small steps. I'm glad you chose to connect with me.",
            "You are heard and you are seen. Sometimes solitude feels like loneliness, but they are different. What kind of connection do you miss the most?"
        ]
    },
    "sleep": {
        "keywords": ["sleep", "insomnia", "awake", "tired", "exhausted", "nightmare", "dream", "can't sleep"],
        "responses": [
            "It's so hard to cope when we aren't rested. Racing thoughts often keep us up. Would you like to try a quick visualization to help quiet your mind?",
            "Insomnia can be so frustrating. If you've been lying in bed for a while, sometimes getting up and doing something calming for 10 minutes helps reset the brain.",
            "Your mind sounds very active. Let's try to focus on just your breathing for a moment. Inhale peace, exhale tension."
        ]
    },
    "relationships": {
        "keywords": ["partner", "boyfriend", "girlfriend", "husband", "wife", "breakup", "broke up", "ex", "date", "cheat", "fighting", "argument"],
        "responses": [
            "Relationships are complex and can bring up our deepest insecurities. It sounds like you're hurting. What do you feel is the main issue right now?",
            "It's painful when we feel disconnected from those we care about. Remember that you can only control your own actions and reactions. How are you taking care of you?",
            "Heartbreak is a valid form of grief. Give yourself permission to mourn the relationship or the trust that was broken."
        ]
    },
    "self_esteem": {
        "keywords": ["ugly", "stupid", "hate myself", "failure", "worthless", "dumb", "useless"],
        "responses": [
            "I hear you saying hurtful things about yourself. If a friend spoke to you that way, what would you say to them? You deserve that same kindness.",
            "You are being very hard on yourself. Failure is an event, not a person. You are valuable simply because you exist.",
            "That is your inner critic speaking, not the truth. Let's look for one piece of evidence that contradicts that negative thought."
        ]
    },
    "greeting": {
        "keywords": ["hello", "hi", "hey", "greetings", "morning", "evening", "start"],
        "responses": [
            "Hello. I'm Serenity. I'm here to provide a safe, non-judgmental space for you to explore your thoughts and feelings. How are you today?",
            "Hi there. I'm listening. Whether you want to vent, problem-solve, or just chat, I'm here. What's on your mind?",
            "Welcome. This is a safe space. How can I support you right now?"
        ]
    },
    "gratitude": {
        "keywords": ["thank", "thanks", "helpful", "good bot", "appreciate"],
        "responses": [
            "You're remarkably kind. I'm just glad I could be here for you.",
            "It is my honor to listen. Thank you for trusting me with your thoughts.",
            "I appreciate you letting me help. Remember to acknowledge your own strength in reaching out."
        ]
    }
}

GENERIC_REFLECTIONS = [
    "I'm listening deeply. Could you tell me a bit more about what that feels like for you?",
    "That sounds like a lot to navigate. How is this impacting your day-to-day life?",
    "I hear the emotion in your words. I'm right here with you.",
    "Thank you for sharing that. It helps me understand your world better. What do you think you need most right now?",
    "It seems like this is really weighing on you. Let's take it one step at a time.",
    "Take your time. There is no rush here. I am with you.",
    "I sense this is important to you. I am here to support you.",
    "Your feelings are valid. Would you like to explore that further?"
]

CRISIS_RESPONSE = "I'm very concerned about what you're sharing. Please know that you're not alone, and there is help available. You might consider reaching out to a crisis counselor—they're available 24/7. In the US, you can call or text 988. If you're outside the US, please contact your local emergency services. Would you like to talk more about what's on your mind?"

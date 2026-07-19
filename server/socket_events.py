from flask import request
from flask_socketio import emit, join_room, leave_room
import random
import string

# In-memory storage for active rooms/users (for prototype)
# In production, use Redis or MongoDB
rooms = {} 
users = {}
room_dummies = {}
active_simulation_rooms = set()
room_user_count = {}

def get_room_dummies(room):
    if room not in room_dummies:
        # Generate 3 consistent dummy users for this room
        adjectives = ["Calm", "Peaceful", "Silent", "Hidden", "Quiet", "Bright"]
        nouns = ["Soul", "Mind", "River", "Tree", "Star", "Cloud"]
        room_dummies[room] = [
            f"{random.choice(adjectives)}{random.choice(nouns)}{random.randint(10, 99)}"
            for _ in range(3)
        ]
    return room_dummies[room]

def generate_anonymous_name():
    adjectives = ["Blue", "Calm", "Silent", "Hidden", "Peaceful", "Quiet"]
    nouns = ["Soul", "Mind", "River", "Tree", "Star", "Cloud"]
    return f"{random.choice(adjectives)}{random.choice(nouns)}{random.randint(10, 99)}"

def register_socket_events(socketio, chatbot):
    
    @socketio.on('connect')
    def handle_connect():
        print(f"Client connected: {request.sid}")

    @socketio.on('join_room')
    def handle_join_room(data):
        room = data.get('room')
        username = generate_anonymous_name()
        
        users[request.sid] = {"username": username, "room": room}
        join_room(room)
        
        room_user_count[room] = room_user_count.get(room, 0) + 1
        
        # Get or create dummy users for this room
        dummies = get_room_dummies(room)
        
        # Inject fabricated recent history so it feels like an ongoing chat
        recent_history_messages = [
            "honestly just trying to breathe through it",
            "yeah i totally get that feeling", 
            "did anyone else find that grounding technique helpful?",
            "im just taking it hour by hour today",
            "i feel like the weekends are sometimes harder tbh",
            "sending love to whoever needs it rn ❤️",
            "does listening to music help anyone else here?",
            "just taking a moment to reset my mind",
            "feeling a little better after venting earlier"
        ]
        num_history = random.randint(2, 3)
        history_dummies = random.sample(dummies, k=min(len(dummies), num_history))
        history_msgs = random.sample(recent_history_messages, k=num_history)
        
        for i in range(num_history):
            emit('message', {
                'user': history_dummies[i],
                'text': history_msgs[i],
                'type': 'user'
            }, room=request.sid)
            socketio.sleep(0.1) # Small delay for order
        
        # 1. Announce system status
        emit('message', {
            'user': 'System',
            'text': f'Welcome to {room} support. There are {len(dummies)} others here.',
            'type': 'system'
        }, room=request.sid)

        # 2. Announce the user joined to everyone
        emit('message', {
            'user': 'System',
            'text': f'{username} has joined the {room} room.',
            'type': 'system'
        }, room=room)
        
        emit('user_joined', {'username': username}, room=request.sid)

        if room not in active_simulation_rooms:
            active_simulation_rooms.add(room)
            def simulate_active_chat():
                while room in active_simulation_rooms and room_user_count.get(room, 0) > 0:
                    socketio.sleep(random.uniform(15.0, 35.0))
                    
                    if room not in active_simulation_rooms or room_user_count.get(room, 0) <= 0:
                        break
                        
                    sim_dummies = get_room_dummies(room)
                    speaker = random.choice(sim_dummies)
                    
                    socketio.emit('typing_start', {'user': speaker}, room=room)
                    socketio.sleep(random.uniform(2.0, 4.0))
                    socketio.emit('typing_stop', room=room)
                    
                    organic_messages = [
                        "has anyone tried meditation lately? been thinking about it",
                        "just taking it one day at a time right now",
                        "hope everyone is having a decent day",
                        "been feeling a bit overwhelmed today, just wanted to say hi",
                        "remember to drink water and take a breather guys",
                        "going for a walk really helped me clear my head earlier",
                        "anyone else struggling to focus today?",
                        "just checking in, hope things are okay",
                        "sending positive vibes to everyone here ✨",
                        "it's okay not to be okay sometimes"
                    ]
                    
                    socketio.emit('message', {
                        'user': speaker,
                        'text': random.choice(organic_messages),
                        'type': 'user'
                    }, room=room)
                    
                    if random.random() < 0.4:
                        socketio.sleep(random.uniform(2.0, 5.0))
                        responder = random.choice([d for d in sim_dummies if d != speaker])
                        
                        socketio.emit('typing_start', {'user': responder}, room=room)
                        socketio.sleep(random.uniform(1.0, 3.0))
                        socketio.emit('typing_stop', room=room)
                        
                        peer_reactions = [
                            "i totally agree with that",
                            "yesss so true",
                            "feel you on that one",
                            "thanks for sharing that ❤️",
                            "i needed to hear that tbh",
                            "fr it's been a tough week",
                            "🫂",
                            "we got this together"
                        ]
                        
                        socketio.emit('message', {
                            'user': responder,
                            'text': random.choice(peer_reactions),
                            'type': 'user'
                        }, room=room)

            socketio.start_background_task(simulate_active_chat)

        # 3. Have a dummy user greet the newcomer after a short delay
        def greet():
            # Initial delay before starting to "type"
            socketio.sleep(1.0)
            greeter = random.choice(dummies)
            
            # Emit typing indicator
            emit('typing_start', {'user': greeter}, room=room)
            socketio.sleep(2.0)
            emit('typing_stop', room=room)

            emit('message', {
                'user': greeter,
                'text': f"Hi {username}! Glad you're here.",
                'type': 'user'
            }, room=room)
        
        socketio.start_background_task(greet)

    @socketio.on('send_message')
    def handle_message(data):
        user_data = users.get(request.sid)
        if user_data:
            room = user_data['room']
            username = user_data['username']
            message = data.get('text')
            
            # Basic moderation (placeholder)
            forbidden = ["hate", "kill"]
            if any(word in message.lower() for word in forbidden):
                emit('message', {
                    'user': 'System', 
                    'text': 'Message blocked due to inappropriate content.',
                    'type': 'system'
                }, room=request.sid)
                return

            emit('message', {
                'user': username,
                'text': message,
                'type': 'user'
            }, room=room)

            # Simulated response from dummy users
            def simulate_responses():
                dummies = get_room_dummies(room)
                # Map ID to human name for AI context
                room_names = {
                    "anxiety": "Anxiety Support",
                    "depression": "Depression Support",
                    "stress": "Stress Relief",
                    "general": "Safe Space"
                }
                readable_room = room_names.get(room, "Support Group")

                # Higher chance of more responses
                num_responses = random.choices([1, 2, 3], weights=[50, 40, 10])[0]
                
                responding_dummies = random.sample(dummies, k=num_responses)
                
                for i, dummy in enumerate(responding_dummies):
                    # Natural gap between responses
                    socketio.sleep(random.uniform(1.0, 3.0))
                    
                    # Start typing
                    emit('typing_start', {'user': dummy}, room=room)
                    
                    # Typing speed based on message complexity placeholder
                    socketio.sleep(random.uniform(2.0, 4.0))
                    
                    # Stop typing
                    emit('typing_stop', room=room)
                    
                    # Get the high-quality human response
                    peer_text = chatbot.get_peer_response(message, dummy, readable_room)
                    
                    emit('message', {
                        'user': dummy,
                        'text': peer_text,
                        'type': 'user'
                    }, room=room)
                    
                    # Periodic peer engagement
                    if random.random() < 0.2:
                        socketio.sleep(2)
                        reactor = random.choice([d for d in dummies if d != dummy])
                        peer_reactions = ["i agree", "so true", "❤️", "exactly", "preach", "fr", "man i feel that"]
                        emit('message', {
                            'user': reactor,
                            'text': random.choice(peer_reactions),
                            'type': 'user'
                        }, room=room)

            socketio.start_background_task(simulate_responses)

    @socketio.on('chat_with_ai')
    def handle_ai_chat(data):
        user_message = data.get('text')
        user_data = users.get(request.sid)
        
        if user_data:
            room = user_data['room']
            username = user_data['username']
            
            # 1. Fetch history from MongoDB
            history = chatbot.chat_log_model.get_recent_history(room)
            
            # 2. Get AI Response with context
            response_data = chatbot.get_response(user_message, history=history)
            
            # 3. Log user message to MongoDB
            chatbot.chat_log_model.log_message(
                room_id=room,
                user_id=username,
                message=user_message,
                role='user',
                emotion=response_data['detected_emotion']
            )
            
            # 4. Log AI response to MongoDB
            chatbot.chat_log_model.log_message(
                room_id=room,
                user_id="Serenity",
                message=response_data['response'],
                role='assistant',
                emotion=response_data['detected_emotion']
            )
            
            emit('ai_response', {
                'text': response_data['response'],
                'emotion': response_data['detected_emotion']
            })
        else:
            # Fallback if user not in a room session
            response_data = chatbot.get_response(user_message)
            emit('ai_response', {
                'text': response_data['response'],
                'emotion': response_data['detected_emotion']
            })

    @socketio.on('disconnect')
    def handle_disconnect():
        user_data = users.pop(request.sid, None)
        if user_data:
            room = user_data['room']
            leave_room(room)
            
            if room in room_user_count:
                room_user_count[room] -= 1
                if room_user_count[room] <= 0:
                    active_simulation_rooms.discard(room)
                    
            emit('message', {
                'user': 'System',
                'text': f"{user_data['username']} has left.",
                'type': 'system'
            }, room=room)

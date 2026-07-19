import React, { useState, useEffect, useRef } from 'react';
import { useParams, Link } from 'react-router-dom';
import io from 'socket.io-client';
import { Send, Users, ArrowLeft } from 'lucide-react';

const ChatRoom = () => {
    const { roomId } = useParams();
    const [socket, setSocket] = useState(null);
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [username, setUsername] = useState('Anonymous');
    const [typingUser, setTypingUser] = useState(null);
    const messagesEndRef = useRef(null);

    useEffect(() => {
        // Connect to Socket.IO
        const newSocket = io('/', {
            path: '/socket.io', // Vite proxy handles the connection to backend
        });

        setSocket(newSocket);

        // Join Room
        newSocket.emit('join_room', { room: roomId });

        // Listeners
        newSocket.on('message', (message) => {
            setMessages((prev) => [...prev, message]);
        });

        newSocket.on('user_joined', (data) => {
            setUsername(data.username);
        });

        newSocket.on('typing_start', (data) => {
            if (data.user !== username) setTypingUser(data.user);
        });

        newSocket.on('typing_stop', () => {
            setTypingUser(null);
        });

        return () => newSocket.disconnect();
    }, [roomId]);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    const sendMessage = (e) => {
        e.preventDefault();
        if (input.trim() && socket) {
            socket.emit('send_message', { text: input });
            setInput('');
        }
    };

    const getRoomName = (id) => {
        const names = {
            anxiety: "Anxiety Support",
            depression: "Depression Support",
            stress: "Stress Relief",
            general: "Safe Space"
        };
        return names[id] || "Chat Room";
    };

    return (
        <div className="flex flex-col h-screen overflow-hidden">
            {/* Header */}
            <header className="glass-panel m-4 mb-0 p-6 flex justify-between items-center z-10 shadow-xl border-t-2 border-white/60">
                <div className="flex items-center gap-4">
                    <Link to="/rooms" className="p-3 bg-slate-100/50 hover:bg-indigo-50 rounded-2xl text-slate-500 hover:text-indigo-600 transition-all duration-300 border border-transparent hover:border-indigo-100 shadow-sm">
                        <ArrowLeft size={20} />
                    </Link>
                    <div>
                        <h1 className="text-2xl font-black bg-gradient-to-r from-indigo-600 to-blue-600 bg-clip-text text-transparent flex items-center gap-3 tracking-tight">
                            <Users size={24} className="text-indigo-500" />
                            {getRoomName(roomId)}
                        </h1>
                        <p className="text-[10px] font-black tracking-widest text-emerald-500 flex items-center gap-1.5 uppercase mt-1">
                            <span className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse shadow-[0_0_8px_rgba(16,185,129,0.5)]"></span>
                            ACTIVE AS {username}
                        </p>
                    </div>
                </div>
                <div className="hidden md:flex px-4 py-2 rounded-full bg-indigo-50 border border-indigo-100 text-indigo-600 text-[10px] font-black tracking-widest items-center gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-indigo-400"></div>
                    ANONYMOUS ENCRYPTION ACTIVE
                </div>
            </header>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-6 flex flex-col gap-8 custom-scrollbar bg-gradient-to-b from-blue-50/30 to-white">
                {messages.map((msg, idx) => {
                    const isMe = msg.user === username;
                    const isSystem = msg.type === 'system';

                    if (isSystem) {
                        return (
                            <div key={idx} className="flex justify-center animate-slide-up">
                                <span className="text-[10px] font-black tracking-widest uppercase bg-slate-200/50 text-slate-500 px-4 py-2 rounded-full border border-slate-200/50 backdrop-blur-sm">
                                    {msg.text}
                                </span>
                            </div>
                        )
                    }

                    return (
                        <div key={idx} className={`flex flex-col ${isMe ? 'items-end' : 'items-start'} animate-slide-up`} style={{ animationDelay: `${idx * 0.05}s` }}>
                            <div className={`flex items-end gap-3 max-w-[85%] ${isMe ? 'flex-row-reverse' : 'flex-row'}`}>
                                {/* Avatar */}
                                <div className={`w-10 h-10 rounded-2xl flex items-center justify-center shadow-lg transform translate-y-2 shrink-0 ${isMe
                                    ? 'bg-blue-600 text-white'
                                    : 'bg-white text-blue-600 border border-blue-50'
                                    }`}>
                                    {isMe ? '👤' : <Users size={18} />}
                                </div>

                                {/* Bubble Container */}
                                <div className="flex flex-col">
                                    <span className={`text-[10px] font-black text-slate-400 mb-2 px-2 tracking-widest ${isMe ? 'text-right' : 'text-left'}`}>
                                        {isMe ? 'YOU' : msg.user.toUpperCase()}
                                    </span>
                                    <div className={isMe
                                        ? 'chat-bubble-user bg-gradient-to-br from-blue-600 to-cyan-600 shadow-[0_10px_25px_-5px_rgba(37,99,235,0.3)]'
                                        : 'chat-bubble-bot border border-blue-50 shadow-sm'
                                    }>
                                        <p className="font-medium">{msg.text}</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    );
                })}
                <div ref={messagesEndRef} />
            </div>

            {/* Typing Indicator */}
            {typingUser && (
                <div className="px-6 py-2 flex items-center gap-2 text-[10px] font-black tracking-widest text-indigo-500 bg-indigo-50/50 backdrop-blur-sm border-t border-indigo-100/50 italic">
                    <div className="flex gap-1">
                        <span className="w-1.5 h-1.5 bg-indigo-400 rounded-full animate-bounce [animation-delay:-0.3s]"></span>
                        <span className="w-1.5 h-1.5 bg-indigo-400 rounded-full animate-bounce [animation-delay:-0.15s]"></span>
                        <span className="w-1.5 h-1.5 bg-indigo-400 rounded-full animate-bounce"></span>
                    </div>
                    {typingUser.toUpperCase()} IS TYPING...
                </div>
            )}

            {/* Input Area */}
            <div className="p-6 bg-white border-t border-blue-100 shadow-[0_-10px_40px_-15px_rgba(0,0,0,0.05)]">
                <form onSubmit={sendMessage} className="max-w-4xl mx-auto flex gap-3 relative">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder={`Message in ${getRoomName(roomId)}...`}
                        className="flex-1 p-4 bg-neutral-50 rounded-2xl border-2 border-neutral-100 focus:border-blue-300 focus:bg-white outline-none transition-all duration-300 font-medium"
                    />
                    <button
                        type="submit"
                        disabled={!input.trim()}
                        className="p-4 bg-gradient-to-br from-blue-600 to-cyan-600 text-white rounded-2xl hover:from-blue-700 hover:to-cyan-700 shadow-lg hover:shadow-blue-200 transition-all duration-300 disabled:opacity-30 disabled:grayscale active:scale-95"
                    >
                        <Send size={20} />
                    </button>
                </form>
            </div>
        </div>
    );
};

export default ChatRoom;

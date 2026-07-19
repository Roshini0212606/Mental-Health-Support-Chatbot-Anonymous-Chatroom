import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Send, Sparkles, AlertCircle, WifiOff, RefreshCw } from 'lucide-react';
import { Link } from 'react-router-dom';

const Chatbot = () => {
    const [messages, setMessages] = useState([
        { text: "Hello! I'm Serenity, your AI support companion. How are you feeling today?", sender: 'bot', emotion: 'Neutral' }
    ]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const [connectionError, setConnectionError] = useState(false);
    const [retryingMessage, setRetryingMessage] = useState(null);
    const [roomId, setRoomId] = useState('');
    const messagesEndRef = useRef(null);

    useEffect(() => {
        // Get or create a persistent room ID for the user
        let savedRoomId = localStorage.getItem('serenity_room_id');
        if (!savedRoomId) {
            savedRoomId = 'user_' + Math.random().toString(36).substring(2, 15);
            localStorage.setItem('serenity_room_id', savedRoomId);
        }
        setRoomId(savedRoomId);

        // Fetch history for this room
        const fetchHistory = async () => {
            try {
                const response = await axios.get(`/api/history/${savedRoomId}`);
                if (response.data && response.data.length > 0) {
                    setMessages(response.data);
                }
            } catch (error) {
                console.error("Error fetching history:", error);
            }
        };

        fetchHistory();
    }, []);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(scrollToBottom, [messages]);

    const sendMessage = async (e, retryMessage = null) => {
        if (e) e.preventDefault();

        const messageToSend = retryMessage || input;
        if (!messageToSend.trim()) return;

        const userMessage = { text: messageToSend, sender: 'user' };

        if (!retryMessage) {
            setMessages(prev => [...prev, userMessage]);
            setInput('');
        }

        setLoading(true);
        setConnectionError(false);

        try {
            const response = await axios.post('/api/chat', {
                message: messageToSend,
                room_id: roomId
            });

            const botMessage = {
                text: response.data.response,
                sender: 'bot',
                emotion: response.data.detected_emotion
            };
            setMessages(prev => [...prev, botMessage]);
            setRetryingMessage(null);
        } catch (error) {
            console.error("Error sending message:", error);
            setConnectionError(true);
            setRetryingMessage(messageToSend);

            const errorMessage = {
                text: "I'm having trouble connecting to the server right now. Please check if the backend is running and try again.",
                sender: 'bot',
                emotion: 'Error',
                isError: true
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setLoading(false);
        }
    };

    const retryLastMessage = () => {
        if (retryingMessage) {
            // Remove the error message
            setMessages(prev => prev.filter(msg => !msg.isError));
            sendMessage(null, retryingMessage);
        }
    };

    const getEmotionColor = (emotion) => {
        const colors = {
            'Happy': 'text-green-600 bg-green-50',
            'Sad': 'text-blue-600 bg-blue-50',
            'Angry': 'text-red-600 bg-red-50',
            'Anxious': 'text-orange-600 bg-orange-50',
            'Neutral': 'text-gray-600 bg-gray-50',
            'Error': 'text-red-600 bg-red-50'
        };
        return colors[emotion] || 'text-purple-600 bg-purple-50';
    };

    return (
        <div className="flex flex-col h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50">
            {/* Header */}
            <header className="glass-panel m-4 mb-0 p-6 flex justify-between items-center z-10 shadow-xl border-t-2 border-white/60">
                <div className="flex items-center gap-4">
                    <div className="relative">
                        <div className="bg-gradient-to-br from-purple-600 to-indigo-600 p-3 rounded-2xl text-white shadow-lg animate-pop-in">
                            <Sparkles size={24} />
                        </div>
                        <div className={`absolute -bottom-1 -right-1 w-4 h-4 rounded-full border-2 border-white shadow-sm ${connectionError ? 'bg-rose-500' : 'bg-emerald-500'} animate-pulse`}></div>
                    </div>
                    <div>
                        <h1 className="text-2xl font-black text-slate-800 tracking-tight leading-none mb-1">Serenity AI</h1>
                        <div className="flex items-center gap-2">
                            <p className="text-xs font-bold text-slate-400 uppercase tracking-widest">
                                {connectionError ? 'SYSTEM OFFLINE' : 'READY TO LISTEN'}
                            </p>
                            {!connectionError && <span className="flex h-1.5 w-1.5 rounded-full bg-emerald-500"></span>}
                        </div>
                    </div>
                </div>
                <Link to="/" className="flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-100/50 hover:bg-rose-50 text-slate-500 hover:text-rose-600 transition-all font-bold text-xs tracking-widest border border-transparent hover:border-rose-100">
                    LEAVE SESSION
                </Link>
            </header>

            {/* Connection Error Banner */}
            {connectionError && (
                <div className="mx-4 mt-2 p-3 bg-red-50 border border-red-200 rounded-lg flex items-center gap-2 text-red-700 text-sm animate-fade-in">
                    <WifiOff size={16} />
                    <span>Backend connection lost. Make sure Flask server is running on port 5000.</span>
                    {retryingMessage && (
                        <button
                            onClick={retryLastMessage}
                            className="ml-auto flex items-center gap-1 px-3 py-1 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors"
                        >
                            <RefreshCw size={14} />
                            Retry
                        </button>
                    )}
                </div>
            )}

            {/* Chat Area */}
            <div className="flex-1 overflow-y-auto p-6 flex flex-col gap-8 custom-scrollbar">
                {messages.map((msg, index) => (
                    <div
                        key={index}
                        className={`flex flex-col ${msg.sender === 'user' ? 'items-end' : 'items-start'} animate-slide-up`}
                        style={{ animationDelay: `${index * 0.05}s` }}
                    >
                        <div className={`flex items-end gap-3 max-w-[85%] ${msg.sender === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                            {/* Avatar */}
                            <div className={`w-10 h-10 rounded-2xl flex items-center justify-center shadow-lg transform translate-y-2 shrink-0 ${msg.sender === 'user'
                                ? 'bg-indigo-100 text-indigo-600'
                                : 'bg-purple-600 text-white'
                                }`}>
                                {msg.sender === 'user' ? '👤' : <Sparkles size={18} />}
                            </div>

                            {/* Bubble Container */}
                            <div className="flex flex-col">
                                <div className={msg.sender === 'user'
                                    ? 'chat-bubble-user'
                                    : msg.isError
                                        ? 'chat-bubble-bot border-2 border-red-200 bg-red-50 text-red-800'
                                        : 'chat-bubble-bot'
                                }>
                                    <div className="flex items-center gap-2 mb-1 opacity-70">
                                        <span className="text-[10px] font-bold uppercase tracking-widest">
                                            {msg.sender === 'user' ? 'You' : 'Serenity'}
                                        </span>
                                    </div>
                                    {msg.isError && (
                                        <div className="flex items-center gap-2 mb-2 text-red-600 font-bold text-sm">
                                            <AlertCircle size={16} />
                                            <span>CONNECTION LOST</span>
                                        </div>
                                    )}
                                    <p className="leading-relaxed font-medium">{msg.text}</p>
                                </div>
                                {msg.sender === 'bot' && msg.emotion && !msg.isError && (
                                    <div className="flex items-center gap-2 mt-2 ml-2">
                                        <span className={`text-[10px] px-3 py-1 rounded-full font-black uppercase tracking-widest ${getEmotionColor(msg.emotion)} shadow-sm`}>
                                            Detected: {msg.emotion}
                                        </span>
                                    </div>
                                )}

                            </div>
                        </div>
                    </div>
                ))}
                {loading && (
                    <div className="self-start bg-white p-4 rounded-2xl rounded-bl-none shadow-md flex gap-2 animate-fade-in">
                        <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce" style={{ animationDelay: '0s' }}></div>
                        <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                        <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="p-6 bg-white/90 backdrop-blur-xl border-t border-slate-100 shadow-[0_-10px_40px_-15px_rgba(0,0,0,0.05)]">
                <form onSubmit={sendMessage} className="max-w-4xl mx-auto flex items-center gap-4">
                    <div className="relative flex-1">
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder="Type how you're feeling..."
                            className="w-full p-4 rounded-2xl border-2 border-slate-100 focus:border-blue-300 focus:bg-white bg-slate-50 transition-all duration-300 placeholder:text-slate-400 outline-none pr-4 pl-6 text-slate-700 font-medium"
                        />
                    </div>
                    <button
                        type="submit"
                        disabled={!input.trim() || loading}
                        className="p-4 bg-gradient-to-r from-sky-400 to-blue-500 text-white rounded-2xl hover:from-sky-500 hover:to-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 shadow-lg hover:shadow-blue-200 active:scale-95 flex items-center justify-center min-w-[3.5rem]"
                    >
                        {loading ? <RefreshCw size={20} className="animate-spin" /> : <Send size={20} />}
                    </button>
                </form>
                <p className="text-center text-xs text-slate-400 mt-4 font-medium tracking-wide">
                    ✨ AI-powered sanctuary. Not medical advice. For emergencies, call 911.
                </p>
            </div>
        </div>
    );
};

export default Chatbot;

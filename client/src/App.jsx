import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Chatbot from './components/Chatbot';
import ChatRoom from './components/ChatRoom';
import { MessageCircle, Heart, Users, ArrowLeft } from 'lucide-react';

function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-6 text-center relative overflow-hidden">
      {/* Animated background highlights */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-purple-300/30 rounded-full blur-[120px] animate-pulse"></div>
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-blue-300/30 rounded-full blur-[120px] animate-pulse" style={{ animationDelay: '2s' }}></div>

      <div className="relative z-10 max-w-5xl w-full">
        <header className="mb-16 animate-pop-in">
          <div className="inline-block px-4 py-1.5 mb-6 rounded-full bg-white/40 border border-white/60 backdrop-blur-md text-sm font-bold text-purple-700 tracing-widest uppercase">
            Your Personal Mental Health Hub
          </div>
          <h1 className="text-6xl md:text-8xl font-black mb-6 tracking-tight transition-all duration-500 hover:scale-105">
            <span className="gradient-text">Serenity AI</span>
          </h1>
          <p className="text-xl md:text-2xl text-slate-600 mb-0 max-w-3xl mx-auto font-medium leading-relaxed">
            A sanctuary for your thoughts. Experience empathetic AI support or join meaningful conversations with anonymous peers.
          </p>
        </header>

        <div className="flex flex-col md:flex-row gap-10 w-full justify-center perspective-1000">
          {/* AI Chatbot Option */}
          <Link to="/ai-chat" className="flex-1 text-decoration-none group animate-slide-up stagger-1">
            <div className="glass-panel tilt-effect p-10 h-full hover:shadow-2xl flex flex-col items-center border-t-2 border-white/50">
              <div className="w-20 h-20 bg-gradient-to-br from-purple-500 to-indigo-600 rounded-2xl flex items-center justify-center mb-8 shadow-xl group-hover:rotate-12 transition-all duration-500">
                <MessageCircle size={40} color="white" strokeWidth={2.5} />
              </div>
              <h2 className="text-3xl font-extrabold mb-4 text-slate-800">AI Companion</h2>
              <p className="text-slate-500 font-medium leading-relaxed">
                Talk to our intelligent AI 24/7. It listens, understands emotions, and offers personalized grounding techniques.
              </p>
              <div className="mt-8 px-6 py-2 rounded-full bg-purple-600 text-white font-bold opacity-0 group-hover:opacity-100 transition-all transform translate-y-4 group-hover:translate-y-0 shadow-lg">
                Start Chatting
              </div>
            </div>
          </Link>

          {/* Peer Rooms Option */}
          <Link to="/rooms" className="flex-1 text-decoration-none group animate-slide-up stagger-2">
            <div className="glass-panel tilt-effect p-10 h-full hover:shadow-2xl flex flex-col items-center border-t-2 border-white/50">
              <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-cyan-600 rounded-2xl flex items-center justify-center mb-8 shadow-xl group-hover:-rotate-12 transition-all duration-500">
                <Users size={40} color="white" strokeWidth={2.5} />
              </div>
              <h2 className="text-3xl font-extrabold mb-4 text-slate-800">Peer Circles</h2>
              <p className="text-slate-500 font-medium leading-relaxed">
                Join topic-based support rooms. Completely anonymous spaces where you can connect with others who truly understand.
              </p>
              <div className="mt-8 px-6 py-2 rounded-full bg-blue-600 text-white font-bold opacity-0 group-hover:opacity-100 transition-all transform translate-y-4 group-hover:translate-y-0 shadow-lg">
                Join Rooms
              </div>
            </div>
          </Link>
        </div>

        <footer className="mt-20 p-8 glass-panel border-white/30 max-w-2xl mx-auto">
          <div className="flex items-center justify-center gap-3 mb-3 text-purple-600">
            <Heart size={20} fill="currentColor" />
            <span className="font-bold uppercase tracking-wider text-xs">Privacy Guaranteed</span>
          </div>
          <p className="text-slate-500 font-medium text-sm mb-4">Your privacy matters. We do not store personal identifiable data.</p>
          <div className="h-px w-20 bg-slate-200 mx-auto mb-4"></div>
          <p className="text-slate-400 text-xs italic">
            <strong>Disclaimer:</strong> Not a replacement for professional therapy. If you are in crisis, please contact emergency services immediately.
          </p>
        </footer>
      </div>
    </div>
  );
}

function RoomSelection() {
  const rooms = [
    { id: 'anxiety', name: 'Anxiety Support', icon: '😰', desc: 'Find calm in the digital storm.', tag: 'Calm', color: 'blue' },
    { id: 'depression', name: 'Depression Support', icon: '⛈️', desc: 'Gentle light for heavy days.', tag: 'Hope', color: 'indigo' },
    { id: 'stress', name: 'Stress Relief', icon: '😤', desc: 'Exhale the pressure of life.', tag: 'Release', color: 'orange' },
    { id: 'general', name: 'Safe Space', icon: '🕊️', desc: 'Open hearts, open discussion.', tag: 'Community', color: 'teal' },
  ];

  return (
    <div className="min-h-screen p-8 flex flex-col items-center relative overflow-hidden">
      {/* Background blobs */}
      <div className="absolute top-0 right-0 w-96 h-96 bg-blue-200/20 blur-[100px] rounded-full"></div>
      <div className="absolute bottom-0 left-0 w-96 h-96 bg-purple-200/20 blur-[100px] rounded-full"></div>

      <div className="relative z-10 w-full max-w-5xl">
        <Link to="/" className="inline-flex items-center gap-2 group mb-12 px-6 py-3 rounded-2xl bg-white/50 border border-white backdrop-blur-md shadow-sm hover:shadow-md transition-all text-slate-700 font-bold">
          <ArrowLeft size={18} className="group-hover:-translate-x-1 transition-transform" />
          BACK TO HUB
        </Link>

        <div className="mb-14 animate-fade-in">
          <h2 className="text-5xl font-black mb-4">
            <span className="gradient-text">Healing Circles</span>
          </h2>
          <p className="text-slate-500 font-medium max-w-lg leading-relaxed">
            Every room is a sanctuary. Choose the space that resonates with your current journey.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 perspective-1000">
          {rooms.map((room, index) => (
            <Link key={room.id} to={`/room/${room.id}`} className={`block group animate-slide-up stagger-${index + 1}`}>
              <div className="glass-panel tilt-effect p-8 flex items-center gap-6 hover:shadow-2xl border-l-[6px] border-l-transparent hover:border-l-indigo-500 bg-white/40 backdrop-blur-xl">
                <div className="w-20 h-20 flex items-center justify-center bg-white/60 rounded-2xl text-5xl shadow-inner group-hover:scale-110 transition-transform duration-500">
                  {room.icon}
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <h3 className="text-2xl font-extrabold text-slate-800">{room.name}</h3>
                    <span className={`px-2 py-0.5 rounded-md text-[10px] font-black uppercase tracking-tighter ${room.color === 'blue' ? 'bg-blue-50 text-blue-500' :
                      room.color === 'indigo' ? 'bg-indigo-50 text-indigo-500' :
                        room.color === 'orange' ? 'bg-orange-50 text-orange-500' :
                          'bg-teal-50 text-teal-500'
                      }`}>
                      {room.tag}
                    </span>
                  </div>
                  <p className="text-slate-500 font-medium text-sm leading-relaxed group-hover:text-slate-700 transition-colors">
                    {room.desc}
                  </p>
                </div>
                <div className="w-10 h-10 rounded-full bg-slate-100 flex items-center justify-center text-slate-400 group-hover:bg-indigo-600 group-hover:text-white transition-all transform group-hover:translate-x-1">
                  →
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/ai-chat" element={<Chatbot />} />
        <Route path="/rooms" element={<RoomSelection />} />
        <Route path="/room/:roomId" element={<ChatRoom />} />
      </Routes>
    </Router>
  );
}

export default App;

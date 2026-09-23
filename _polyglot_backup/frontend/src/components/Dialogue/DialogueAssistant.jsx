import React, { useState, useRef, useEffect } from 'react';
import { 
  MessageSquare, 
  Send, 
  Volume2, 
  Mic, 
  MicOff, 
  User, 
  RotateCcw,
  Sparkles 
} from 'lucide-react';
import { sendDialogueMessage } from '../../api/client';

export default function DialogueAssistant({ languages }) {
  const [speakerALang, setSpeakerALang] = useState("en");
  const [speakerBLang, setSpeakerBLang] = useState("hi");
  
  const [messages, setMessages] = useState([
    {
      id: "init-1",
      speaker: "speaker_a",
      original_text: "Hello! Welcome to our university campus.",
      source_lang: "en",
      translated_text: "नमस्ते! हमारे विश्वविद्यालय परिसर में आपका स्वागत है।",
      target_lang: "hi",
      transliteration: "namaste! hamaare vishvavidyaalay parisar mein aapaka svaagat hai.",
      timestamp: "10:00:15"
    },
    {
      id: "init-2",
      speaker: "speaker_b",
      original_text: "धन्यवाद! मुझे कंप्यूटर साइंस विभाग जाना है।",
      source_lang: "hi",
      translated_text: "Thank you! I have to go to the Computer Science department.",
      target_lang: "en",
      transliteration: "dhanyavaad! mujhe kampyootar sains vibhaag jaana hai.",
      timestamp: "10:00:45"
    }
  ]);

  const [inputA, setInputA] = useState("");
  const [inputB, setInputB] = useState("");
  const [loading, setLoading] = useState(false);

  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (speaker, text) => {
    if (!text.trim() || loading) return;

    setLoading(true);
    try {
      const msg = await sendDialogueMessage({
        speaker,
        text,
        speaker_a_lang: speakerALang,
        speaker_b_lang: speakerBLang
      });

      setMessages((prev) => [...prev, msg]);
      if (speaker === "speaker_a") setInputA("");
      else setInputB("");

      // Auto speak the translation
      speak(msg.translated_text, msg.target_lang);
    } catch (err) {
      console.error("Dialogue message error", err);
    } finally {
      setLoading(false);
    }
  };

  const speak = (text, lang) => {
    if (!('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    if (lang === "hi") utterance.lang = "hi-IN";
    else if (lang === "mr") utterance.lang = "mr-IN";
    else utterance.lang = "en-US";
    window.speechSynthesis.speak(utterance);
  };

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fadeIn">
      
      {/* Header & Language Selectors */}
      <div className="mb-6 p-4 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              <MessageSquare className="w-5 h-5 text-brand-400" />
              Live Bilingual Dialogue Assistant
            </h2>
            <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-brand-500/10 text-brand-400 border border-brand-500/20">
              Slides 3 & 9
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Real-time conversational cross-language translation between two participants
          </p>
        </div>

        {/* Language pairing controls */}
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <span className="text-xs font-bold text-indigo-400">Speaker A:</span>
            <select
              value={speakerALang}
              onChange={(e) => setSpeakerALang(e.target.value)}
              className="bg-slate-950 border border-slate-800 rounded-lg px-2.5 py-1 text-xs text-white"
            >
              {languages.filter(l => l.code !== "auto").map(l => (
                <option key={l.code} value={l.code}>{l.name}</option>
              ))}
            </select>
          </div>

          <span className="text-slate-600">⇄</span>

          <div className="flex items-center gap-2">
            <span className="text-xs font-bold text-emerald-400">Speaker B:</span>
            <select
              value={speakerBLang}
              onChange={(e) => setSpeakerBLang(e.target.value)}
              className="bg-slate-950 border border-slate-800 rounded-lg px-2.5 py-1 text-xs text-white"
            >
              {languages.filter(l => l.code !== "auto").map(l => (
                <option key={l.code} value={l.code}>{l.name}</option>
              ))}
            </select>
          </div>

          <button
            onClick={() => setMessages([])}
            className="p-1.5 rounded-lg border border-slate-800 text-slate-400 hover:text-white hover:bg-slate-800 transition text-xs"
            title="Clear Chat"
          >
            <RotateCcw className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Chat Messages Area */}
      <div className="h-[460px] overflow-y-auto p-4 rounded-2xl bg-slate-950/70 border border-slate-800 mb-6 space-y-4">
        {messages.map((m) => {
          const isA = m.speaker === "speaker_a";
          return (
            <div
              key={m.id}
              className={`flex flex-col ${isA ? "items-start" : "items-end"}`}
            >
              <div className="flex items-center gap-1.5 mb-1 text-[11px] text-slate-500">
                <User className="w-3 h-3" />
                <span className="font-semibold text-slate-400">
                  {isA ? `Speaker A (${m.source_lang.toUpperCase()})` : `Speaker B (${m.source_lang.toUpperCase()})`}
                </span>
                <span>• {m.timestamp}</span>
              </div>

              <div
                className={`max-w-xl rounded-2xl p-4 shadow-lg border ${
                  isA
                    ? "bg-slate-900 border-indigo-900/40 text-slate-100 rounded-tl-none"
                    : "bg-emerald-950/30 border-emerald-800/40 text-slate-100 rounded-tr-none"
                }`}
              >
                {/* Original utterance */}
                <p className="text-sm font-semibold mb-2">{m.original_text}</p>

                {/* Translated output */}
                <div className="pt-2 border-t border-slate-800/80 flex items-start justify-between gap-3">
                  <div>
                    <span className="text-[10px] uppercase font-bold text-slate-500 tracking-wider block">
                      Translated ({m.target_lang.toUpperCase()}):
                    </span>
                    <p className={`text-sm font-medium ${isA ? "text-cyan-300" : "text-emerald-300"}`}>
                      {m.translated_text}
                    </p>
                    {m.transliteration && (
                      <p className="text-[11px] text-slate-400 font-mono mt-0.5">
                        {m.transliteration}
                      </p>
                    )}
                  </div>

                  <button
                    onClick={() => speak(m.translated_text, m.target_lang)}
                    className="p-1.5 rounded-lg text-slate-400 hover:text-white bg-slate-800/50 hover:bg-slate-800 transition shrink-0"
                    title="Speak translation"
                  >
                    <Volume2 className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            </div>
          );
        })}
        <div ref={messagesEndRef} />
      </div>

      {/* Dual Input Panels: Speaker A on Left, Speaker B on Right */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        
        {/* Speaker A Input */}
        <div className="p-3.5 rounded-2xl bg-slate-900 border border-indigo-900/40 shadow-xl">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-bold text-indigo-400 flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-indigo-500" />
              Speaker A ({speakerALang.toUpperCase()})
            </span>
          </div>
          <div className="flex items-center gap-2">
            <input
              type="text"
              value={inputA}
              onChange={(e) => setInputA(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSendMessage("speaker_a", inputA)}
              placeholder={`Type in ${speakerALang.toUpperCase()}...`}
              className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-indigo-500"
            />
            <button
              onClick={() => handleSendMessage("speaker_a", inputA)}
              disabled={loading || !inputA.trim()}
              className="px-3 py-2 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white rounded-xl text-xs font-semibold flex items-center gap-1 transition shadow-md"
            >
              <Send className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        {/* Speaker B Input */}
        <div className="p-3.5 rounded-2xl bg-slate-900 border border-emerald-900/40 shadow-xl">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-bold text-emerald-400 flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-emerald-500" />
              Speaker B ({speakerBLang.toUpperCase()})
            </span>
          </div>
          <div className="flex items-center gap-2">
            <input
              type="text"
              value={inputB}
              onChange={(e) => setInputB(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSendMessage("speaker_b", inputB)}
              placeholder={`Type in ${speakerBLang.toUpperCase()}...`}
              className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-emerald-500"
            />
            <button
              onClick={() => handleSendMessage("speaker_b", inputB)}
              disabled={loading || !inputB.trim()}
              className="px-3 py-2 bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-white rounded-xl text-xs font-semibold flex items-center gap-1 transition shadow-md"
            >
              <Send className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

      </div>

    </div>
  );
}

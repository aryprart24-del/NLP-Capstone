import React, { useState, useEffect, useRef } from 'react';
import { 
  ArrowRightLeft, 
  Volume2, 
  Copy, 
  Check, 
  Sparkles, 
  Mic, 
  MicOff, 
  Trash2, 
  Bookmark, 
  Layers, 
  Sliders, 
  HelpCircle,
  ExternalLink,
  ChevronRight
} from 'lucide-react';
import { translateText, detectLanguage, addPhrase } from '../../api/client';
import LinguisticPanel from './LinguisticPanel';

export default function StudioView({ languages, onInspectInPipeline }) {
  const [sourceText, setSourceText] = useState("मुझे कल कॉलेज जाना है।");
  const [sourceLang, setSourceLang] = useState("hi");
  const [targetLang, setTargetLang] = useState("en");
  const [tone, setTone] = useState("neutral");
  const [domain, setDomain] = useState("general");
  
  const [translatedText, setTranslatedText] = useState("");
  const [transliteration, setTransliteration] = useState("");
  const [sourceTransliteration, setSourceTransliteration] = useState("");
  const [backTranslation, setBackTranslation] = useState("");
  const [fidelityScore, setFidelityScore] = useState(null);
  const [linguisticInsights, setLinguisticInsights] = useState(null);
  const [engineUsed, setEngineUsed] = useState("");
  
  const [loading, setLoading] = useState(false);
  const [copiedTarget, setCopiedTarget] = useState(false);
  const [copiedSource, setCopiedSource] = useState(false);
  const [savedToPhrasebook, setSavedToPhrasebook] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [detectedInfo, setDetectedInfo] = useState(null);

  const speechRecognitionRef = useRef(null);

  // Quick benchmark presentation samples
  const SAMPLE_PILLS = [
    { label: "Slide 9: Hindi Input", text: "मुझे कल कॉलेज जाना है।", src: "hi", tgt: "en" },
    { label: "Slide 6: English Transformer", text: "I am going to college.", src: "en", tgt: "hi" },
    { label: "Slide 7: Hinglish Code-Switch", text: "Mujhe kal college jaana hai because exam conduct ho raha hai.", src: "auto", tgt: "en" },
    { label: "Slide 7: Idiom Disambiguation", text: "It is raining cats and dogs outside.", src: "en", tgt: "hi" },
    { label: "Slide 2: NLP Definition", text: "Natural Language Processing enables computers to understand human language.", src: "en", tgt: "hi" },
    { label: "Regional: Marathi Sample", text: "तुम्ही उद्या कॉलेजला येणार का?", src: "mr", tgt: "en" }
  ];

  // Perform translation
  const handleTranslate = async (overrideText = null, overrideSrc = null, overrideTgt = null) => {
    const textToUse = overrideText !== null ? overrideText : sourceText;
    const srcToUse = overrideSrc !== null ? overrideSrc : sourceLang;
    const tgtToUse = overrideTgt !== null ? overrideTgt : targetLang;

    if (!textToUse.trim()) {
      setTranslatedText("");
      setTransliteration("");
      setLinguisticInsights(null);
      return;
    }

    setLoading(true);
    try {
      const res = await translateText({
        text: textToUse,
        source_lang: srcToUse,
        target_lang: tgtToUse,
        tone: tone,
        domain: domain,
        include_back_translation: true,
        include_linguistic_analysis: true
      });

      setTranslatedText(res.translated_text);
      setTransliteration(res.transliteration || "");
      setSourceTransliteration(res.source_transliteration || "");
      setBackTranslation(res.back_translation || "");
      setFidelityScore(res.fidelity_score);
      setLinguisticInsights(res.linguistic_insights);
      setEngineUsed(res.engine_used);
      setSavedToPhrasebook(false);
    } catch (err) {
      console.error(err);
      alert("Translation failed. Please ensure the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  // Swap Languages
  const handleSwap = () => {
    if (sourceLang === "auto") return;
    const newSrc = targetLang;
    const newTgt = sourceLang;
    const newText = translatedText || sourceText;
    setSourceLang(newSrc);
    setTargetLang(newTgt);
    setSourceText(newText);
    handleTranslate(newText, newSrc, newTgt);
  };

  // Speech-to-Text (STT) via Web Speech API
  const toggleSpeechRecognition = () => {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      alert("Speech recognition is not supported in this browser. Please try Chrome/Edge.");
      return;
    }

    if (isListening) {
      speechRecognitionRef.current?.stop();
      setIsListening(false);
      return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    speechRecognitionRef.current = recognition;

    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = sourceLang === "hi" ? "hi-IN" : sourceLang === "mr" ? "mr-IN" : "en-US";

    recognition.onstart = () => setIsListening(true);
    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setSourceText(transcript);
      handleTranslate(transcript, sourceLang, targetLang);
    };
    recognition.onerror = (e) => {
      console.error("Speech recognition error:", e);
      setIsListening(false);
    };
    recognition.onend = () => setIsListening(false);

    recognition.start();
  };

  // Text-to-Speech (TTS)
  const speakText = (text, lang) => {
    if (!('speechSynthesis' in window)) {
      alert("Speech synthesis is not supported in this browser.");
      return;
    }
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    if (lang === "hi") utterance.lang = "hi-IN";
    else if (lang === "mr") utterance.lang = "mr-IN";
    else if (lang === "es") utterance.lang = "es-ES";
    else if (lang === "fr") utterance.lang = "fr-FR";
    else utterance.lang = "en-US";
    utterance.rate = 0.95;
    window.speechSynthesis.speak(utterance);
  };

  // Copy to clipboard
  const handleCopy = (text, setCopiedState) => {
    navigator.clipboard.writeText(text);
    setCopiedState(true);
    setTimeout(() => setCopiedState(false), 2000);
  };

  // Save to Phrasebook
  const handleSavePhrasebook = async () => {
    if (!sourceText.trim() || !translatedText.trim()) return;
    try {
      await addPhrase({
        source_text: sourceText,
        source_lang: sourceLang,
        translated_text: translatedText,
        target_lang: targetLang,
        category: domain !== "general" ? domain.toUpperCase() : "Studio",
        notes: `Tone: ${tone}`
      });
      setSavedToPhrasebook(true);
      setTimeout(() => setSavedToPhrasebook(false), 2500);
    } catch (e) {
      console.error("Failed to save phrase", e);
    }
  };

  // Initial translation on component mount
  useEffect(() => {
    handleTranslate();
  }, []);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fadeIn">
      
      {/* Presentation Sample Pills */}
      <div className="mb-6">
        <div className="flex items-center gap-2 mb-2 text-xs font-semibold uppercase tracking-wider text-slate-400">
          <Sparkles className="w-3.5 h-3.5 text-brand-400" />
          <span>Quick Demo Examples from Aryan's Presentation:</span>
        </div>
        <div className="flex flex-wrap gap-2">
          {SAMPLE_PILLS.map((pill, idx) => (
            <button
              key={idx}
              onClick={() => {
                setSourceText(pill.text);
                setSourceLang(pill.src);
                setTargetLang(pill.tgt);
                handleTranslate(pill.text, pill.src, pill.tgt);
              }}
              className="text-xs px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-brand-900/40 border border-slate-800 hover:border-brand-500/40 text-slate-300 hover:text-white transition flex items-center gap-1.5 shadow-sm"
            >
              <span>{pill.label}</span>
              <ChevronRight className="w-3 h-3 text-slate-500" />
            </button>
          ))}
        </div>
      </div>

      {/* Control Bar: Language Selectors, Tone, Domain */}
      <div className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 mb-6 shadow-xl">
        <div className="flex flex-wrap items-center justify-between gap-4">
          
          {/* Language Pair Selectors */}
          <div className="flex items-center gap-3 flex-1 min-w-[280px]">
            {/* Source Lang */}
            <div className="flex-1">
              <label className="block text-[11px] font-semibold uppercase tracking-wider text-slate-400 mb-1">
                Source Language
              </label>
              <select
                value={sourceLang}
                onChange={(e) => {
                  setSourceLang(e.target.value);
                  handleTranslate(sourceText, e.target.value, targetLang);
                }}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-brand-500 transition"
              >
                {languages.map((l) => (
                  <option key={l.code} value={l.code}>
                    {l.name} {l.native_name !== l.name ? `(${l.native_name})` : ''}
                  </option>
                ))}
              </select>
            </div>

            {/* Swap Button */}
            <div className="pt-5">
              <button
                onClick={handleSwap}
                disabled={sourceLang === "auto"}
                title="Swap source and target languages"
                className={`p-2.5 rounded-xl border border-slate-800 bg-slate-950 text-slate-300 hover:text-white hover:border-brand-500 transition shadow-sm ${
                  sourceLang === "auto" ? "opacity-40 cursor-not-allowed" : "hover:scale-105 active:scale-95"
                }`}
              >
                <ArrowRightLeft className="w-4 h-4" />
              </button>
            </div>

            {/* Target Lang */}
            <div className="flex-1">
              <label className="block text-[11px] font-semibold uppercase tracking-wider text-slate-400 mb-1">
                Target Language
              </label>
              <select
                value={targetLang}
                onChange={(e) => {
                  setTargetLang(e.target.value);
                  handleTranslate(sourceText, sourceLang, e.target.value);
                }}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-brand-500 transition"
              >
                {languages.filter(l => l.code !== "auto").map((l) => (
                  <option key={l.code} value={l.code}>
                    {l.name} {l.native_name !== l.name ? `(${l.native_name})` : ''}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Tone & Domain Modifiers */}
          <div className="flex items-center gap-3">
            {/* Tone Selector */}
            <div>
              <label className="block text-[11px] font-semibold uppercase tracking-wider text-slate-400 mb-1">
                Tone / Persona
              </label>
              <select
                value={tone}
                onChange={(e) => {
                  setTone(e.target.value);
                  handleTranslate();
                }}
                className="bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-brand-500 transition"
              >
                <option value="neutral">Neutral / Standard</option>
                <option value="formal">Formal / Respectful (आप)</option>
                <option value="casual">Casual / Friendly</option>
                <option value="academic">Academic / Scholarly</option>
                <option value="diplomatic">Diplomatic / Courteous</option>
                <option value="simplified">Simplified / Clear</option>
              </select>
            </div>

            {/* Domain Glossary */}
            <div>
              <label className="block text-[11px] font-semibold uppercase tracking-wider text-slate-400 mb-1">
                Domain Glossary
              </label>
              <select
                value={domain}
                onChange={(e) => {
                  setDomain(e.target.value);
                  handleTranslate();
                }}
                className="bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-brand-500 transition"
              >
                <option value="general">General (No Glossary)</option>
                <option value="tech">Software & AI Tech</option>
                <option value="medical">Medical & Healthcare</option>
                <option value="legal">Legal & Contracts</option>
                <option value="business">Business & Finance</option>
                <option value="tourism">Tourism & Travel</option>
              </select>
            </div>
          </div>

        </div>
      </div>

      {/* Main Dual-Pane Translation Workbench */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Source Text Card */}
        <div className="flex flex-col bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-xl">
          <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-3">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
              Input Text
            </span>
            <div className="flex items-center gap-2">
              {sourceText && (
                <button
                  onClick={() => setSourceText("")}
                  className="p-1.5 rounded-lg text-slate-400 hover:text-rose-400 hover:bg-slate-800 transition"
                  title="Clear input"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              )}
              <button
                onClick={toggleSpeechRecognition}
                className={`p-1.5 rounded-lg transition ${
                  isListening 
                    ? "bg-rose-500/20 text-rose-400 border border-rose-500/40 animate-pulse" 
                    : "text-slate-400 hover:text-white hover:bg-slate-800"
                }`}
                title={isListening ? "Listening... click to stop" : "Voice Input (Speech-to-Text)"}
              >
                {isListening ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
              </button>
              <button
                onClick={() => speakText(sourceText, sourceLang)}
                disabled={!sourceText.trim()}
                className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 disabled:opacity-30 transition"
                title="Listen (Text-to-Speech)"
              >
                <Volume2 className="w-4 h-4" />
              </button>
              <button
                onClick={() => handleCopy(sourceText, setCopiedSource)}
                disabled={!sourceText.trim()}
                className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 disabled:opacity-30 transition"
                title="Copy source text"
              >
                {copiedSource ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
              </button>
            </div>
          </div>

          <textarea
            value={sourceText}
            onChange={(e) => setSourceText(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
                e.preventDefault();
                handleTranslate();
              }
            }}
            placeholder="Type or paste text to translate... (Ctrl+Enter to run)"
            rows={7}
            className="w-full flex-1 bg-transparent text-white placeholder-slate-500 resize-none focus:outline-none text-base leading-relaxed"
          />

          {/* Source Phonetic Transliteration */}
          {sourceTransliteration && (
            <div className="mt-2 p-2.5 rounded-xl bg-slate-950/70 border border-slate-800/80 text-xs">
              <span className="text-[10px] uppercase font-bold text-slate-500 tracking-wider block mb-0.5">
                Phonetic Transliteration (Pronunciation Guide)
              </span>
              <p className="text-cyan-300 font-mono">{sourceTransliteration}</p>
            </div>
          )}

          {/* Footer of Source Card */}
          <div className="flex items-center justify-between pt-3 border-t border-slate-800 mt-4 text-xs text-slate-400">
            <span>{sourceText.length} characters • {sourceText.trim().split(/\s+/).filter(Boolean).length} words</span>
            <div className="flex items-center gap-2">
              <button
                onClick={() => onInspectInPipeline(sourceText, sourceLang, targetLang)}
                className="text-xs text-brand-400 hover:text-brand-300 flex items-center gap-1 font-medium transition"
              >
                <Layers className="w-3.5 h-3.5" />
                <span>Inspect Pipeline</span>
              </button>
              <button
                onClick={() => handleTranslate()}
                disabled={loading || !sourceText.trim()}
                className="px-4 py-2 bg-brand-600 hover:bg-brand-500 disabled:opacity-50 text-white rounded-xl font-semibold shadow-md shadow-brand-600/20 transition flex items-center gap-2"
              >
                {loading ? (
                  <>
                    <div className="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                    <span>Translating...</span>
                  </>
                ) : (
                  <>
                    <Sparkles className="w-3.5 h-3.5" />
                    <span>Translate</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Target Translation Card */}
        <div className="flex flex-col bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-xl relative">
          <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-3">
            <div className="flex items-center gap-2">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
                Translated Output
              </span>
              {engineUsed && (
                <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
                  {engineUsed}
                </span>
              )}
            </div>
            
            <div className="flex items-center gap-2">
              <button
                onClick={handleSavePhrasebook}
                disabled={!translatedText.trim()}
                className={`p-1.5 rounded-lg border transition ${
                  savedToPhrasebook 
                    ? "bg-amber-500/20 text-amber-300 border-amber-500/40" 
                    : "border-slate-800 text-slate-400 hover:text-amber-400 hover:bg-slate-800 disabled:opacity-30"
                }`}
                title="Save to Phrasebook (Favorites)"
              >
                <Bookmark className="w-4 h-4" />
              </button>
              <button
                onClick={() => speakText(translatedText, targetLang)}
                disabled={!translatedText.trim()}
                className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 disabled:opacity-30 transition"
                title="Listen (Text-to-Speech)"
              >
                <Volume2 className="w-4 h-4" />
              </button>
              <button
                onClick={() => handleCopy(translatedText, setCopiedTarget)}
                disabled={!translatedText.trim()}
                className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 disabled:opacity-30 transition"
                title="Copy translated text"
              >
                {copiedTarget ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
              </button>
            </div>
          </div>

          <div className="flex-1 min-h-[140px]">
            {loading ? (
              <div className="h-full flex items-center justify-center text-slate-500 text-sm gap-2">
                <div className="w-5 h-5 border-2 border-brand-500 border-t-transparent rounded-full animate-spin" />
                <span>Running neural machine translation...</span>
              </div>
            ) : translatedText ? (
              <p className="text-white text-lg leading-relaxed font-medium">
                {translatedText}
              </p>
            ) : (
              <p className="text-slate-600 text-sm italic">
                Translation will appear here...
              </p>
            )}
          </div>

          {/* Target Phonetic Transliteration (e.g. Devanagari to Roman) */}
          {transliteration && (
            <div className="mt-3 p-2.5 rounded-xl bg-slate-950/70 border border-slate-800/80 text-xs">
              <span className="text-[10px] uppercase font-bold text-slate-500 tracking-wider block mb-0.5">
                Phonetic Transliteration
              </span>
              <p className="text-emerald-300 font-mono">{transliteration}</p>
            </div>
          )}

          {/* Footer of Target Card */}
          <div className="flex items-center justify-between pt-3 border-t border-slate-800 mt-4 text-xs text-slate-400">
            <span>{translatedText.length} characters • {translatedText.trim().split(/\s+/).filter(Boolean).length} words</span>
            {fidelityScore !== null && (
              <span className="text-xs font-semibold text-emerald-400 flex items-center gap-1">
                Semantic Fidelity: {Math.round(fidelityScore * 100)}%
              </span>
            )}
          </div>
        </div>

      </div>

      {/* Linguistic Intelligence & Back-Translation Panel */}
      <LinguisticPanel 
        insights={linguisticInsights}
        fidelityScore={fidelityScore}
        backTranslation={backTranslation}
        sourceText={sourceText}
      />

    </div>
  );
}

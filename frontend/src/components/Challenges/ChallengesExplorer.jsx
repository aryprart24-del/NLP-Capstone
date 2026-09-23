import React, { useState, useEffect } from 'react';
import { 
  AlertTriangle, 
  HelpCircle, 
  ArrowRight, 
  CheckCircle2, 
  XCircle, 
  Sparkles, 
  Cpu, 
  Play,
  Lightbulb
} from 'lucide-react';
import { fetchChallenges } from '../../api/client';

export default function ChallengesExplorer({ onTestInStudio }) {
  const [challenges, setChallenges] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState("ALL");

  useEffect(() => {
    async function load() {
      try {
        const data = await fetchChallenges();
        setChallenges(data);
      } catch (err) {
        console.error("Failed to load challenges", err);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  const categories = ["ALL", "AMBIGUITY", "CONTEXT", "IDIOMS & SLANG", "LOW-RESOURCE", "CULTURE", "CODE-SWITCHING"];

  const filtered = selectedCategory === "ALL" 
    ? challenges 
    : challenges.filter(c => c.category === selectedCategory);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fadeIn">
      
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-2">
          <h2 className="text-xl font-black text-white tracking-tight flex items-center gap-2">
            <AlertTriangle className="w-6 h-6 text-amber-400" />
            Major NLP Translation Challenges Explorer
          </h2>
          <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/20">
            Slide 7 Presentation Focus
          </span>
        </div>
        <p className="text-xs text-slate-400 mt-1">
          Why high-quality multilingual translation remains difficult and how modern NLP solves them.
        </p>
        
        {/* Core Thesis Banner */}
        <div className="mt-4 p-3.5 rounded-xl bg-gradient-to-r from-brand-950/60 via-slate-900 to-indigo-950/60 border border-brand-500/30 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <Lightbulb className="w-5 h-5 text-amber-400 shrink-0" />
            <span className="text-sm font-semibold text-slate-200">
              Fundamental NLP Principle: <span className="text-cyan-300 font-bold">Language ≠ Just Words → Context + Culture + Meaning</span>
            </span>
          </div>
        </div>
      </div>

      {/* Category Filter Pills */}
      <div className="flex flex-wrap gap-2 mb-6">
        {categories.map((cat) => (
          <button
            key={cat}
            onClick={() => setSelectedCategory(cat)}
            className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition ${
              selectedCategory === cat
                ? "bg-brand-600 text-white shadow-md shadow-brand-600/30"
                : "bg-slate-900 text-slate-400 hover:text-white border border-slate-800"
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Challenges Grid */}
      {loading ? (
        <div className="text-center py-12 text-slate-500 text-sm">
          Loading challenge modules...
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filtered.map((item) => (
            <div 
              key={item.id}
              className="flex flex-col bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-xl hover:border-slate-700 transition"
            >
              {/* Category Badge & Title */}
              <div className="flex items-center justify-between mb-3">
                <span className="text-[10px] font-black uppercase tracking-wider px-2 py-0.5 rounded-full bg-slate-800 text-brand-400 border border-slate-700">
                  {item.category}
                </span>
                <span className="text-[11px] font-mono text-slate-500">
                  {item.source_lang.toUpperCase()} → {item.target_lang.toUpperCase()}
                </span>
              </div>

              <h3 className="text-base font-bold text-white mb-1.5">
                {item.title}
              </h3>
              <p className="text-xs text-slate-400 leading-relaxed mb-4">
                {item.description}
              </p>

              {/* Sample Input */}
              <div className="p-2.5 rounded-xl bg-slate-950 border border-slate-800 mb-3 text-xs">
                <span className="text-[10px] uppercase font-bold text-slate-500 tracking-wider block mb-1">
                  Example Input
                </span>
                <p className="font-semibold text-white">{item.example_input}</p>
              </div>

              {/* Literal (Error) vs Contextual (Correct) */}
              <div className="space-y-2 mb-4 text-xs">
                <div className="p-2 rounded-lg bg-rose-950/20 border border-rose-900/30">
                  <div className="flex items-center gap-1.5 text-rose-400 font-semibold mb-0.5 text-[11px]">
                    <XCircle className="w-3.5 h-3.5" /> Naive / Literal Word-for-Word:
                  </div>
                  <p className="text-slate-300 text-[11px]">{item.literal_translation}</p>
                </div>

                <div className="p-2 rounded-lg bg-emerald-950/20 border border-emerald-900/30">
                  <div className="flex items-center gap-1.5 text-emerald-400 font-semibold mb-0.5 text-[11px]">
                    <CheckCircle2 className="w-3.5 h-3.5" /> Contextual NLP Translation:
                  </div>
                  <p className="text-emerald-200 font-medium text-[11px]">{item.contextual_nlp_translation}</p>
                </div>
              </div>

              {/* Technical NLP Solution Mechanism */}
              <div className="mt-auto pt-3 border-t border-slate-800/80">
                <div className="flex items-start gap-1.5 text-[11px] text-slate-300 mb-3">
                  <Cpu className="w-3.5 h-3.5 text-indigo-400 mt-0.5 shrink-0" />
                  <span><b>Solution:</b> {item.solution_mechanism}</span>
                </div>

                <button
                  onClick={() => onTestInStudio(item.example_input, item.source_lang, item.target_lang)}
                  className="w-full py-2 bg-slate-950 hover:bg-brand-600/20 border border-slate-800 hover:border-brand-500/40 text-brand-300 hover:text-white rounded-xl text-xs font-semibold flex items-center justify-center gap-1.5 transition"
                >
                  <Play className="w-3 h-3" />
                  <span>Test in Studio</span>
                </button>
              </div>

            </div>
          ))}
        </div>
      )}

    </div>
  );
}

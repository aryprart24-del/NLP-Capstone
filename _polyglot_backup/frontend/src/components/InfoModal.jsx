import React from 'react';
import { X, GraduationCap, Award, BookOpen, Layers, CheckCircle2 } from 'lucide-react';

export default function InfoModal({ isOpen, onClose }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-fadeIn">
      <div className="relative w-full max-w-2xl bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-2xl overflow-hidden">
        
        {/* Glow accent */}
        <div className="absolute top-0 right-0 w-64 h-64 bg-brand-500/10 rounded-full blur-3xl pointer-events-none" />

        {/* Header */}
        <div className="flex items-center justify-between border-b border-slate-800 pb-4 mb-4">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-xl bg-brand-500/10 text-brand-400 border border-brand-500/20">
              <GraduationCap className="w-6 h-6" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-white">Project Presentation Context</h2>
              <p className="text-xs text-slate-400">B.Tech • AI & Data Science Capstone Project</p>
            </div>
          </div>
          <button 
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content Body */}
        <div className="space-y-4 text-sm text-slate-300">
          
          {/* Metadata Cards */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <div className="p-3 bg-slate-950/50 rounded-xl border border-slate-800/80">
              <span className="text-[10px] uppercase font-bold text-slate-500 tracking-wider">Subject</span>
              <p className="text-xs font-semibold text-slate-200 mt-0.5">NLP</p>
            </div>
            <div className="p-3 bg-slate-950/50 rounded-xl border border-slate-800/80">
              <span className="text-[10px] uppercase font-bold text-slate-500 tracking-wider">Program</span>
              <p className="text-xs font-semibold text-slate-200 mt-0.5">B.Tech • AI & DS</p>
            </div>
            <div className="p-3 bg-slate-950/50 rounded-xl border border-slate-800/80">
              <span className="text-[10px] uppercase font-bold text-slate-500 tracking-wider">Presented By</span>
              <p className="text-xs font-semibold text-brand-400 mt-0.5">Aryan</p>
            </div>
            <div className="p-3 bg-slate-950/50 rounded-xl border border-slate-800/80">
              <span className="text-[10px] uppercase font-bold text-slate-500 tracking-wider">Institution</span>
              <p className="text-xs font-semibold text-slate-200 mt-0.5">D.Y. Patil University</p>
            </div>
          </div>

          {/* Presentation Core Thesis */}
          <div className="p-4 bg-brand-950/30 border border-brand-800/30 rounded-xl">
            <h3 className="font-semibold text-brand-300 mb-1 flex items-center gap-1.5">
              <BookOpen className="w-4 h-4" /> Core Research Theme
            </h3>
            <p className="text-xs leading-relaxed text-slate-300">
              "How Natural Language Processing enables communication across languages — moving from simple word-to-word substitution to meaning-preserving, contextual and cultural translation."
            </p>
            <div className="mt-2 text-[11px] font-mono text-cyan-300 bg-cyan-950/40 p-2 rounded border border-cyan-800/40">
              Language ≠ Just Words → Context + Culture + Meaning
            </div>
          </div>

          {/* Key Implemented Modules */}
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2 flex items-center gap-1.5">
              <Layers className="w-3.5 h-3.5" /> Modules Implemented from Presentation
            </h4>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
              <div className="flex items-start gap-2 p-2 bg-slate-950/40 rounded-lg border border-slate-800/60">
                <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                <div>
                  <span className="font-medium text-white">Interactive Pipeline (Slides 4 & 6)</span>
                  <p className="text-[11px] text-slate-400">Subwords, Embeddings, Multi-Head Attention & Beam Search.</p>
                </div>
              </div>
              <div className="flex items-start gap-2 p-2 bg-slate-950/40 rounded-lg border border-slate-800/60">
                <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                <div>
                  <span className="font-medium text-white">6 Major Challenges (Slide 7)</span>
                  <p className="text-[11px] text-slate-400">Ambiguity, Context, Idioms, Low-Resource, Culture, Code-Switching.</p>
                </div>
              </div>
              <div className="flex items-start gap-2 p-2 bg-slate-950/40 rounded-lg border border-slate-800/60">
                <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                <div>
                  <span className="font-medium text-white">Transliteration & TTS (Slides 3 & 9)</span>
                  <p className="text-[11px] text-slate-400">Devanagari ⇄ Latin phonetic transliteration & speech audio.</p>
                </div>
              </div>
              <div className="flex items-start gap-2 p-2 bg-slate-950/40 rounded-lg border border-slate-800/60">
                <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                <div>
                  <span className="font-medium text-white">Live Bilingual Dialogue (Slide 3)</span>
                  <p className="text-[11px] text-slate-400">Split-screen real-time conversation between two speakers.</p>
                </div>
              </div>
            </div>
          </div>

        </div>

        {/* Footer */}
        <div className="mt-6 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-brand-600 hover:bg-brand-500 text-white rounded-xl text-xs font-semibold shadow-md transition"
          >
            Close & Continue
          </button>
        </div>

      </div>
    </div>
  );
}

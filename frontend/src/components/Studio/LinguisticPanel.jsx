import React, { useState } from 'react';
import { Sparkles, Brain, BookOpen, Tag, Compass, ChevronDown, ChevronUp, AlertCircle } from 'lucide-react';

export default function LinguisticPanel({ insights, fidelityScore, backTranslation, sourceText }) {
  const [isOpen, setIsOpen] = useState(true);

  if (!insights && !backTranslation) return null;

  const fidelityPercentage = Math.round((fidelityScore || 0.9) * 100);
  const getFidelityColor = (score) => {
    if (score >= 85) return 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20';
    if (score >= 65) return 'text-amber-400 bg-amber-500/10 border-amber-500/20';
    return 'text-rose-400 bg-rose-500/10 border-rose-500/20';
  };

  return (
    <div className="mt-6 rounded-2xl bg-slate-900/90 border border-slate-800 p-5 shadow-xl transition-all">
      {/* Header with Toggle */}
      <div 
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center justify-between cursor-pointer select-none pb-3 border-b border-slate-800"
      >
        <div className="flex items-center gap-2.5">
          <div className="p-1.5 rounded-lg bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
            <Brain className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              Linguistic Intelligence & Semantic Evaluation
              <span className="text-[10px] uppercase font-semibold px-2 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                NLP Assistance
              </span>
            </h3>
            <p className="text-xs text-slate-400">
              Grammar analysis, back-translation fidelity, and cultural nuance notes
            </p>
          </div>
        </div>
        <button className="text-slate-400 hover:text-white transition">
          {isOpen ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
        </button>
      </div>

      {isOpen && (
        <div className="mt-4 space-y-5 animate-fadeIn">
          
          {/* Back-Translation & Semantic Preservation Fidelity Gauge */}
          {backTranslation && (
            <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800/80">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-2">
                <span className="text-xs font-semibold text-slate-300 flex items-center gap-1.5">
                  <Compass className="w-4 h-4 text-cyan-400" />
                  Semantic Fidelity & Drift Verification (Back-Translation)
                </span>
                <span className={`text-xs font-bold px-2.5 py-1 rounded-full border ${getFidelityColor(fidelityPercentage)}`}>
                  {fidelityPercentage}% Meaning Preserved
                </span>
              </div>

              {/* Progress Bar */}
              <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden mb-3">
                <div 
                  className="h-full bg-gradient-to-r from-brand-500 via-indigo-500 to-emerald-400 rounded-full transition-all duration-700"
                  style={{ width: `${fidelityPercentage}%` }}
                />
              </div>

              {/* Comparison Box */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                <div className="p-2.5 bg-slate-900 rounded-lg border border-slate-800">
                  <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider block mb-1">
                    Original Source
                  </span>
                  <p className="text-slate-200">{sourceText}</p>
                </div>
                <div className="p-2.5 bg-slate-900 rounded-lg border border-slate-800">
                  <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider block mb-1">
                    Back-Translated to Source
                  </span>
                  <p className="text-emerald-300 font-medium">{backTranslation}</p>
                </div>
              </div>
            </div>
          )}

          {/* Grammar & Word-Order Reordering Notes */}
          {insights?.grammar_notes?.length > 0 && (
            <div className="p-3.5 bg-slate-950/50 rounded-xl border border-slate-800/80">
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2 flex items-center gap-1.5">
                <BookOpen className="w-3.5 h-3.5 text-brand-400" /> Syntactic & Grammar Notes
              </h4>
              <ul className="space-y-1.5 text-xs text-slate-300">
                {insights.grammar_notes.map((note, idx) => (
                  <li key={idx} className="flex items-start gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-brand-400 mt-1.5 shrink-0" />
                    <span>{note}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Cultural & Honorific Nuances */}
          {insights?.cultural_notes?.length > 0 && (
            <div className="p-3.5 bg-slate-950/50 rounded-xl border border-slate-800/80">
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2 flex items-center gap-1.5">
                <Sparkles className="w-3.5 h-3.5 text-amber-400" /> Cultural & Register Notes
              </h4>
              <ul className="space-y-1.5 text-xs text-slate-300">
                {insights.cultural_notes.map((note, idx) => (
                  <li key={idx} className="flex items-start gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-amber-400 mt-1.5 shrink-0" />
                    <span>{note}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Detected Idioms */}
          {insights?.idioms_detected?.length > 0 && (
            <div className="p-3.5 bg-slate-950/50 rounded-xl border border-slate-800/80">
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2 flex items-center gap-1.5">
                <AlertCircle className="w-3.5 h-3.5 text-purple-400" /> Idioms & Context Disambiguation
              </h4>
              <div className="space-y-2">
                {insights.idioms_detected.map((item, idx) => (
                  <div key={idx} className="text-xs bg-slate-900 p-2.5 rounded-lg border border-slate-800">
                    <span className="font-semibold text-purple-300">"{item.idiom}"</span>
                    <p className="text-slate-400 mt-0.5">{item.explanation}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* POS & Subword Token Breakdown */}
          {insights?.tokens?.length > 0 && (
            <div>
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2 flex items-center gap-1.5">
                <Tag className="w-3.5 h-3.5 text-cyan-400" /> Morphological & POS Tag Breakdown
              </h4>
              <div className="flex flex-wrap gap-2">
                {insights.tokens.map((t, idx) => (
                  <div 
                    key={idx} 
                    className="flex flex-col items-center bg-slate-950/80 border border-slate-800 px-2.5 py-1.5 rounded-lg text-center"
                  >
                    <span className="text-xs font-bold text-slate-200">{t.token}</span>
                    <span className="text-[10px] text-cyan-400/90 font-mono mt-0.5">{t.pos}</span>
                    {t.subwords?.length > 1 && (
                      <span className="text-[9px] text-slate-500 font-mono">
                        [{t.subwords.join(', ')}]
                      </span>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

        </div>
      )}
    </div>
  );
}

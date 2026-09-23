import React, { useState, useEffect } from 'react';
import { 
  Workflow, 
  Cpu, 
  Layers, 
  ArrowRight, 
  Play, 
  RefreshCw, 
  Sparkles, 
  Eye, 
  Activity,
  CheckCircle2
} from 'lucide-react';
import { inspectPipeline } from '../../api/client';

export default function PipelineVisualizer({ initialText = "I am going to college.", initialSrc = "en", initialTgt = "hi" }) {
  const [inputText, setInputText] = useState(initialText);
  const [sourceLang, setSourceLang] = useState(initialSrc);
  const [targetLang, setTargetLang] = useState(initialTgt);
  const [pipelineData, setPipelineData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeStep, setActiveStep] = useState(4); // Default to Attention / Transformer
  const [hoveredCell, setHoveredCell] = useState(null);

  const runInspection = async (text = inputText, src = sourceLang, tgt = targetLang) => {
    if (!text.trim()) return;
    setLoading(true);
    try {
      const data = await inspectPipeline({
        text,
        source_lang: src,
        target_lang: tgt
      });
      setPipelineData(data);
    } catch (err) {
      console.error("Pipeline inspection error:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    runInspection(initialText, initialSrc, initialTgt);
  }, []);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fadeIn">
      
      {/* Header */}
      <div className="mb-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-xl font-black text-white tracking-tight flex items-center gap-2">
              <Workflow className="w-6 h-6 text-brand-400" />
              Multilingual Translation Pipeline Inspector
            </h2>
            <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-brand-500/10 text-brand-400 border border-brand-500/20">
              Slides 4 & 6
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Interactive breakdown of the 6-stage NLP pipeline & Transformer Self-Attention mechanism
          </p>
        </div>

        {/* Input Bar */}
        <div className="flex items-center gap-2">
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Type sentence to inspect..."
            className="bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-brand-500 min-w-[260px]"
          />
          <button
            onClick={() => runInspection()}
            disabled={loading}
            className="px-3.5 py-2 bg-brand-600 hover:bg-brand-500 text-white rounded-xl text-xs font-semibold flex items-center gap-1.5 shadow-md transition"
          >
            {loading ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : <Play className="w-3.5 h-3.5" />}
            <span>Run Pipeline</span>
          </button>
        </div>
      </div>

      {/* Preset Slide Demos */}
      <div className="flex flex-wrap items-center gap-2 mb-6">
        <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">Slide Examples:</span>
        <button
          onClick={() => {
            setInputText("I am going to college.");
            setSourceLang("en");
            setTargetLang("hi");
            runInspection("I am going to college.", "en", "hi");
          }}
          className="text-xs px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-800 text-slate-300 hover:text-white hover:border-brand-500/50 transition"
        >
          Slide 6: "I am going to college." (EN → HI)
        </button>
        <button
          onClick={() => {
            setInputText("मुझे कल कॉलेज जाना है।");
            setSourceLang("hi");
            setTargetLang("en");
            runInspection("मुझे कल कॉलेज जाना है।", "hi", "en");
          }}
          className="text-xs px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-800 text-slate-300 hover:text-white hover:border-brand-500/50 transition"
        >
          Slide 9: "मुझे कल कॉलेज जाना है।" (HI → EN)
        </button>
      </div>

      {/* The 6 Pipeline Stages Horizontal Stepper (Slide 4) */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 mb-8">
        {[
          { num: 1, title: "1. INPUT", subtitle: "Text / Speech", icon: "💬" },
          { num: 2, title: "2. DETECT", subtitle: "Source Language", icon: "🌐" },
          { num: 3, title: "3. ENCODE", subtitle: "Tokens & Embeddings", icon: "🧬" },
          { num: 4, title: "4. TRANSLATE", subtitle: "Transformer / NMT", icon: "⚡" },
          { num: 5, title: "5. DECODE", subtitle: "Target Language", icon: "🎯" },
          { num: 6, title: "6. OUTPUT", subtitle: "Assistance & Meaning", icon: "✨" },
        ].map((s) => {
          const isSelected = activeStep === s.num;
          return (
            <button
              key={s.num}
              onClick={() => setActiveStep(s.num)}
              className={`p-3.5 rounded-2xl border text-left transition-all ${
                isSelected
                  ? "bg-brand-600/10 border-brand-500 text-white shadow-lg shadow-brand-500/10 scale-[1.02]"
                  : "bg-slate-900/80 border-slate-800 text-slate-400 hover:border-slate-700 hover:text-slate-200"
              }`}
            >
              <div className="flex items-center justify-between mb-1.5">
                <span className="text-lg">{s.icon}</span>
                <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${
                  isSelected ? "bg-brand-500 text-white" : "bg-slate-800 text-slate-500"
                }`}>
                  Step {s.num}
                </span>
              </div>
              <p className="text-xs font-bold text-white truncate">{s.title}</p>
              <p className="text-[11px] text-slate-400 truncate mt-0.5">{s.subtitle}</p>
            </button>
          );
        })}
      </div>

      {/* Step Detail View & Interactive Attention Heatmap */}
      {pipelineData && (
        <div className="space-y-6">
          
          {/* Active Step Information Box */}
          {pipelineData.steps && (
            <div className="p-5 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl">
              {(() => {
                const curStep = pipelineData.steps.find(s => s.step_number === activeStep) || pipelineData.steps[3];
                return (
                  <div>
                    <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-3">
                      <div className="flex items-center gap-2">
                        <span className="text-xs font-mono font-bold text-brand-400 px-2 py-0.5 rounded bg-brand-500/10 border border-brand-500/20">
                          Step {curStep.step_number} of 6
                        </span>
                        <h3 className="text-base font-bold text-white">{curStep.name}</h3>
                      </div>
                      <span className="text-xs text-slate-400 italic hidden sm:inline">
                        "The goal is meaning-preserving translation, not simple word-to-word substitution."
                      </span>
                    </div>
                    <p className="text-xs text-slate-300 leading-relaxed mb-4">
                      {curStep.description}
                    </p>

                    {/* Step-specific visual output */}
                    <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 font-mono text-xs overflow-x-auto">
                      <pre className="text-emerald-300">
                        {JSON.stringify(curStep.output_data, null, 2)}
                      </pre>
                    </div>
                  </div>
                );
              })()}
            </div>
          )}

          {/* Transformer Architecture Diagram & Cross-Attention Matrix (Slide 6) */}
          <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <Cpu className="w-5 h-5 text-indigo-400" />
                <h3 className="text-base font-bold text-white">
                  Multi-Head Cross-Attention Matrix (Encoder-Decoder Alignment)
                </h3>
              </div>
              <span className="text-xs text-slate-400">
                Slide 6: Attention Mechanism identifying relevant context
              </span>
            </div>

            <p className="text-xs text-slate-400 mb-4">
              Hover over heatmap cells to see the dynamic attention weights assigned between source tokens (Encoder) and target tokens (Decoder).
            </p>

            {/* Heatmap Matrix Table */}
            <div className="overflow-x-auto pb-2">
              <table className="min-w-full border-collapse text-xs">
                <thead>
                  <tr>
                    <th className="p-2 border border-slate-800 bg-slate-950 text-slate-500 font-mono text-left">
                      Source \ Target
                    </th>
                    {pipelineData.decoder_tokens.map((tgtToken, j) => (
                      <th 
                        key={j} 
                        className={`p-2 border border-slate-800 bg-slate-950 font-mono text-center font-bold ${
                          hoveredCell?.col === j ? "text-cyan-300 bg-cyan-950/40" : "text-slate-300"
                        }`}
                      >
                        {tgtToken}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {pipelineData.encoder_tokens.map((srcToken, i) => (
                    <tr key={i}>
                      <td className={`p-2 border border-slate-800 bg-slate-950 font-mono font-bold ${
                        hoveredCell?.row === i ? "text-indigo-300 bg-indigo-950/40" : "text-slate-300"
                      }`}>
                        {srcToken}
                      </td>
                      {pipelineData.decoder_tokens.map((tgtToken, j) => {
                        const weight = pipelineData.attention_matrix[i]?.[j] || 0.05;
                        const isHovered = hoveredCell?.row === i && hoveredCell?.col === j;
                        const opacity = Math.min(1.0, Math.max(0.15, weight * 2.2));

                        return (
                          <td
                            key={j}
                            onMouseEnter={() => setHoveredCell({ row: i, col: j, weight, src: srcToken, tgt: tgtToken })}
                            onMouseLeave={() => setHoveredCell(null)}
                            style={{
                              backgroundColor: `rgba(99, 102, 241, ${opacity})`
                            }}
                            className={`p-2.5 border border-slate-800 text-center font-mono transition-all cursor-pointer ${
                              isHovered ? "ring-2 ring-cyan-400 font-black text-white" : "text-slate-200"
                            }`}
                          >
                            {weight.toFixed(2)}
                          </td>
                        );
                      })}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Hover Tooltip Info */}
            {hoveredCell && (
              <div className="mt-4 p-3 rounded-xl bg-slate-950 border border-brand-500/40 flex items-center justify-between text-xs animate-fadeIn">
                <div className="flex items-center gap-2">
                  <Activity className="w-4 h-4 text-cyan-400" />
                  <span className="text-slate-300">
                    Source Token: <b className="text-white">"{hoveredCell.src}"</b> → Target Token: <b className="text-white">"{hoveredCell.tgt}"</b>
                  </span>
                </div>
                <div className="text-cyan-300 font-mono font-bold">
                  Attention Weight: {(hoveredCell.weight * 100).toFixed(1)}%
                </div>
              </div>
            )}
          </div>

        </div>
      )}

    </div>
  );
}

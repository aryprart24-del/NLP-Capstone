import React, { useState } from 'react';
import { 
  FileText, 
  UploadCloud, 
  Download, 
  CheckCircle2, 
  RefreshCw, 
  FileCode, 
  Table, 
  Eye 
} from 'lucide-react';
import { uploadDocument } from '../../api/client';

export default function DocumentTranslator({ languages }) {
  const [file, setFile] = useState(null);
  const [sourceLang, setSourceLang] = useState("auto");
  const [targetLang, setTargetLang] = useState("hi");
  const [translatedData, setTranslatedData] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleTranslate = async () => {
    if (!file) return;
    setLoading(true);
    try {
      const data = await uploadDocument({
        file,
        source_lang: sourceLang,
        target_lang: targetLang
      });
      setTranslatedData(data);
    } catch (err) {
      console.error("Document translation error", err);
      alert("Failed to translate document. Check format.");
    } finally {
      setLoading(false);
    }
  };

  const downloadTranslatedFile = () => {
    if (!translatedData) return;
    const blob = new Blob([translatedData.translated_content], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `translated_${translatedData.filename}`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fadeIn">
      
      {/* Header */}
      <div className="mb-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              <FileText className="w-5 h-5 text-brand-400" />
              Document & Batch Localization
            </h2>
            <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-brand-500/10 text-brand-400 border border-brand-500/20">
              Slide 8
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Translates markdown, JSON, CSV, and plain text files while preserving schema and syntax tags
          </p>
        </div>

        {/* Translation Language Controls */}
        <div className="flex items-center gap-3">
          <div>
            <label className="block text-[10px] font-bold uppercase text-slate-400 mb-1">
              Source
            </label>
            <select
              value={sourceLang}
              onChange={(e) => setSourceLang(e.target.value)}
              className="bg-slate-900 border border-slate-800 rounded-xl px-2.5 py-1.5 text-xs text-white"
            >
              {languages.map(l => (
                <option key={l.code} value={l.code}>{l.name}</option>
              ))}
            </select>
          </div>

          <span className="text-slate-600 mt-4">→</span>

          <div>
            <label className="block text-[10px] font-bold uppercase text-slate-400 mb-1">
              Target
            </label>
            <select
              value={targetLang}
              onChange={(e) => setTargetLang(e.target.value)}
              className="bg-slate-900 border border-slate-800 rounded-xl px-2.5 py-1.5 text-xs text-white"
            >
              {languages.filter(l => l.code !== "auto").map(l => (
                <option key={l.code} value={l.code}>{l.name}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Upload Dropzone */}
      <div className="p-6 rounded-2xl bg-slate-900/90 border border-slate-800 shadow-xl mb-6">
        <div className="border-2 border-dashed border-slate-800 hover:border-brand-500/50 rounded-xl p-8 text-center transition">
          <UploadCloud className="w-10 h-10 text-brand-400 mx-auto mb-3" />
          <p className="text-sm font-semibold text-white mb-1">
            Upload document to translate
          </p>
          <p className="text-xs text-slate-400 mb-4">
            Supports <span className="text-brand-300 font-mono">.txt</span>, <span className="text-brand-300 font-mono">.md</span>, <span className="text-brand-300 font-mono">.json</span>, <span className="text-brand-300 font-mono">.csv</span>
          </p>

          <input
            type="file"
            id="doc-upload"
            onChange={handleFileChange}
            accept=".txt,.md,.json,.csv"
            className="hidden"
          />
          <div className="flex items-center justify-center gap-3">
            <label
              htmlFor="doc-upload"
              className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-xl text-xs font-semibold cursor-pointer transition"
            >
              Browse Computer
            </label>
            {file && (
              <button
                onClick={handleTranslate}
                disabled={loading}
                className="px-4 py-2 bg-brand-600 hover:bg-brand-500 text-white rounded-xl text-xs font-semibold flex items-center gap-1.5 shadow-md transition"
              >
                {loading ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : <CheckCircle2 className="w-3.5 h-3.5" />}
                <span>Translate Document</span>
              </button>
            )}
          </div>

          {file && (
            <p className="text-xs text-emerald-400 mt-3 font-mono">
              Selected: {file.name} ({(file.size / 1024).toFixed(1)} KB)
            </p>
          )}
        </div>
      </div>

      {/* Side-by-Side Document Preview */}
      {translatedData && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
              Translation Result ({translatedData.line_count} lines processed)
            </span>
            <button
              onClick={downloadTranslatedFile}
              className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-xs font-semibold flex items-center gap-1.5 shadow-md transition"
            >
              <Download className="w-4 h-4" />
              <span>Download Translated File</span>
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-4 rounded-xl bg-slate-900 border border-slate-800">
              <span className="text-[11px] font-bold text-slate-500 uppercase tracking-wider block mb-2">
                Original Document ({translatedData.filename})
              </span>
              <pre className="font-mono text-xs text-slate-300 h-96 overflow-y-auto bg-slate-950 p-3 rounded-lg border border-slate-800/80">
                {translatedData.original_content}
              </pre>
            </div>

            <div className="p-4 rounded-xl bg-slate-900 border border-slate-800">
              <span className="text-[11px] font-bold text-emerald-400 uppercase tracking-wider block mb-2">
                Translated Document ({targetLang.toUpperCase()})
              </span>
              <pre className="font-mono text-xs text-emerald-200 h-96 overflow-y-auto bg-slate-950 p-3 rounded-lg border border-slate-800/80">
                {translatedData.translated_content}
              </pre>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}

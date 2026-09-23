import React, { useState, useEffect } from 'react';
import { 
  Bookmark, 
  Search, 
  Volume2, 
  Trash2, 
  Download, 
  Plus, 
  Tag, 
  ExternalLink 
} from 'lucide-react';
import { fetchPhrasebook, deletePhrase, addPhrase } from '../../api/client';

export default function PhrasebookView() {
  const [phrases, setPhrases] = useState([]);
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("all");
  const [loading, setLoading] = useState(true);

  const [showAddModal, setShowAddModal] = useState(false);
  const [newSource, setNewSource] = useState("");
  const [newSrcLang, setNewSrcLang] = useState("hi");
  const [newTarget, setNewTarget] = useState("");
  const [newTgtLang, setNewTgtLang] = useState("en");
  const [newCategory, setNewCategory] = useState("Academic");

  const loadPhrases = async () => {
    setLoading(true);
    try {
      const data = await fetchPhrasebook(category === "all" ? null : category);
      setPhrases(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadPhrases();
  }, [category]);

  const handleDelete = async (id) => {
    try {
      await deletePhrase(id);
      setPhrases(phrases.filter(p => p.id !== id));
    } catch (e) {
      console.error(e);
    }
  };

  const handleAddSubmit = async (e) => {
    e.preventDefault();
    if (!newSource.trim() || !newTarget.trim()) return;

    try {
      await addPhrase({
        source_text: newSource,
        source_lang: newSrcLang,
        translated_text: newTarget,
        target_lang: newTgtLang,
        category: newCategory,
        notes: "Custom entry"
      });
      setShowAddModal(false);
      setNewSource("");
      setNewTarget("");
      loadPhrases();
    } catch (e) {
      console.error(e);
    }
  };

  const speak = (text, lang) => {
    if (!('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    if (lang === "hi") utterance.lang = "hi-IN";
    else utterance.lang = "en-US";
    window.speechSynthesis.speak(utterance);
  };

  const exportCSV = () => {
    if (!phrases.length) return;
    const rows = [["ID", "Source Text", "Source Lang", "Translated Text", "Target Lang", "Category"]];
    phrases.forEach(p => {
      rows.push([p.id, `"${p.source_text.replace(/"/g, '""')}"`, p.source_lang, `"${p.translated_text.replace(/"/g, '""')}"`, p.target_lang, p.category]);
    });
    const csvContent = "data:text/csv;charset=utf-8," + rows.map(e => e.join(",")).join("\n");
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "polyglot_phrasebook.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const filtered = phrases.filter(p => 
    p.source_text.toLowerCase().includes(search.toLowerCase()) ||
    p.translated_text.toLowerCase().includes(search.toLowerCase())
  );

  const categories = ["all", "Academic", "Greetings", "Travel / Healthcare", "Tech", "General"];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fadeIn">
      
      {/* Header */}
      <div className="mb-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              <Bookmark className="w-5 h-5 text-amber-400" />
              Multilingual Phrasebook & Lexicon
            </h2>
            <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/20">
              SQLite Persistence
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Bookmarked phrases, curated domain expressions, and flashcard learning
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowAddModal(true)}
            className="px-3.5 py-2 bg-brand-600 hover:bg-brand-500 text-white rounded-xl text-xs font-semibold flex items-center gap-1.5 shadow-md transition"
          >
            <Plus className="w-4 h-4" />
            <span>Add Phrase</span>
          </button>
          <button
            onClick={exportCSV}
            disabled={!phrases.length}
            className="px-3.5 py-2 bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 hover:text-white rounded-xl text-xs font-semibold flex items-center gap-1.5 transition"
          >
            <Download className="w-4 h-4" />
            <span>Export CSV</span>
          </button>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4 mb-6">
        {/* Categories */}
        <div className="flex flex-wrap gap-1.5">
          {categories.map((c) => (
            <button
              key={c}
              onClick={() => setCategory(c)}
              className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition ${
                category === c
                  ? "bg-amber-500/20 text-amber-300 border border-amber-500/40"
                  : "bg-slate-900 text-slate-400 hover:text-white border border-slate-800"
              }`}
            >
              {c.toUpperCase()}
            </button>
          ))}
        </div>

        {/* Search */}
        <div className="relative w-full sm:w-64">
          <Search className="w-4 h-4 text-slate-500 absolute left-3 top-2.5" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search saved phrases..."
            className="w-full bg-slate-900 border border-slate-800 rounded-xl pl-9 pr-3 py-2 text-xs text-white focus:outline-none focus:border-amber-500"
          />
        </div>
      </div>

      {/* Phrase Cards */}
      {loading ? (
        <div className="text-center py-12 text-slate-500 text-sm">
          Loading phrasebook...
        </div>
      ) : filtered.length === 0 ? (
        <div className="text-center py-12 text-slate-500 text-sm bg-slate-900/50 rounded-2xl border border-slate-800">
          No phrases found in this category.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filtered.map((item) => (
            <div
              key={item.id}
              className="p-4 rounded-2xl bg-slate-900/90 border border-slate-800 hover:border-slate-700 shadow-xl flex flex-col justify-between transition"
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-slate-800 text-amber-400 border border-slate-700">
                    {item.category}
                  </span>
                  <div className="flex items-center gap-1.5 text-slate-500 text-[11px] font-mono">
                    <span>{item.source_lang.toUpperCase()}</span>
                    <span>→</span>
                    <span>{item.target_lang.toUpperCase()}</span>
                  </div>
                </div>

                <p className="text-sm font-bold text-white mb-1.5">
                  {item.source_text}
                </p>

                <p className="text-xs text-emerald-300 font-medium mb-3">
                  {item.translated_text}
                </p>

                {item.notes && (
                  <p className="text-[11px] text-slate-400 italic mb-2">
                    Note: {item.notes}
                  </p>
                )}
              </div>

              <div className="pt-3 border-t border-slate-800/80 flex items-center justify-between">
                <button
                  onClick={() => speak(item.translated_text, item.target_lang)}
                  className="p-1.5 rounded-lg text-slate-400 hover:text-white bg-slate-950 border border-slate-800 transition"
                  title="Speak"
                >
                  <Volume2 className="w-3.5 h-3.5" />
                </button>
                <button
                  onClick={() => handleDelete(item.id)}
                  className="p-1.5 rounded-lg text-slate-400 hover:text-rose-400 bg-slate-950 border border-slate-800 transition"
                  title="Delete phrase"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Add Phrase Modal */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-fadeIn">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 w-full max-w-md shadow-2xl">
            <h3 className="text-base font-bold text-white mb-4">Add Phrase to Lexicon</h3>
            <form onSubmit={handleAddSubmit} className="space-y-3">
              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-1">Source Text</label>
                <input
                  type="text"
                  required
                  value={newSource}
                  onChange={(e) => setNewSource(e.target.value)}
                  placeholder="e.g. मुझे कल कॉलेज जाना है।"
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-amber-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-1">Translated Text</label>
                <input
                  type="text"
                  required
                  value={newTarget}
                  onChange={(e) => setNewTarget(e.target.value)}
                  placeholder="e.g. I have to go to college tomorrow."
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-amber-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-1">Category</label>
                <select
                  value={newCategory}
                  onChange={(e) => setNewCategory(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-amber-500"
                >
                  <option value="Academic">Academic</option>
                  <option value="Greetings">Greetings</option>
                  <option value="Travel / Healthcare">Travel / Healthcare</option>
                  <option value="Tech">Tech</option>
                  <option value="General">General</option>
                </select>
              </div>

              <div className="pt-4 flex items-center justify-end gap-2">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-xl text-xs font-semibold transition"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-amber-600 hover:bg-amber-500 text-white rounded-xl text-xs font-semibold transition"
                >
                  Save Phrase
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
}

import React from 'react';
import { 
  Languages, 
  Workflow, 
  AlertCircle, 
  MessageSquare, 
  FileText, 
  Bookmark, 
  GraduationCap, 
  Sparkles,
  Info
} from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, onOpenInfo }) {
  const tabs = [
    { id: 'studio', label: 'Translation Studio', icon: Languages, badge: 'NMT' },
    { id: 'pipeline', label: 'Pipeline Inspector', icon: Workflow, badge: 'Transformer' },
    { id: 'challenges', label: 'NLP Challenges', icon: AlertCircle, badge: 'Slide 7' },
    { id: 'dialogue', label: 'Bilingual Dialogue', icon: MessageSquare, badge: 'Live' },
    { id: 'document', label: 'Doc Translator', icon: FileText, badge: 'Files' },
    { id: 'phrasebook', label: 'Phrasebook', icon: Bookmark, badge: 'SQLite' },
  ];

  return (
    <header className="sticky top-0 z-50 border-b border-slate-800 bg-slate-950/80 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Brand & Project Info */}
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-600 via-indigo-600 to-cyan-400 p-0.5 shadow-lg shadow-brand-500/20">
              <div className="w-full h-full bg-slate-950 rounded-[10px] flex items-center justify-center">
                <Sparkles className="w-5 h-5 text-cyan-400 animate-pulse" />
              </div>
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-extrabold text-lg tracking-tight bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
                  PolyGlot NLP
                </span>
                <span className="text-[10px] font-semibold uppercase tracking-wider px-2 py-0.5 rounded-full bg-brand-500/10 text-brand-400 border border-brand-500/20">
                  Assistant
                </span>
              </div>
              <p className="text-xs text-slate-400 hidden sm:block">
                Multilingual NLP Translation Assistant • Aryan
              </p>
            </div>
          </div>

          {/* Navigation Tabs */}
          <nav className="flex items-center space-x-1 overflow-x-auto py-1">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              const isActive = activeTab === tab.id;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-150 whitespace-nowrap ${
                    isActive
                      ? 'bg-brand-600 text-white shadow-md shadow-brand-600/30'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/60'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span>{tab.label}</span>
                  {tab.badge && (
                    <span className={`text-[10px] font-semibold px-1.5 py-0.2 rounded ${
                      isActive ? 'bg-white/20 text-white' : 'bg-slate-800 text-slate-400'
                    }`}>
                      {tab.badge}
                    </span>
                  )}
                </button>
              );
            })}
          </nav>

          {/* Academic Info Action */}
          <div className="flex items-center gap-2">
            <button
              onClick={onOpenInfo}
              className="flex items-center gap-2 px-3 py-1.5 rounded-lg border border-slate-800 hover:border-slate-700 bg-slate-900/50 text-xs text-slate-300 hover:text-white transition"
              title="Project Details & Presentation Info"
            >
              <GraduationCap className="w-4 h-4 text-brand-400" />
              <span className="hidden md:inline font-medium">D.Y. Patil Univ</span>
              <Info className="w-3.5 h-3.5 text-slate-400" />
            </button>
          </div>

        </div>
      </div>
    </header>
  );
}

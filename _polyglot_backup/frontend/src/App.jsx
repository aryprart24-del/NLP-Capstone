import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import InfoModal from './components/InfoModal';
import StudioView from './components/Studio/StudioView';
import PipelineVisualizer from './components/Pipeline/PipelineVisualizer';
import ChallengesExplorer from './components/Challenges/ChallengesExplorer';
import DialogueAssistant from './components/Dialogue/DialogueAssistant';
import DocumentTranslator from './components/Document/DocumentTranslator';
import PhrasebookView from './components/Phrasebook/PhrasebookView';
import { fetchLanguages } from './api/client';
import { GraduationCap, Heart, Github, Sparkles } from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('studio');
  const [isInfoOpen, setIsInfoOpen] = useState(false);
  const [languages, setLanguages] = useState([
    { code: 'auto', name: 'Auto Detect', native_name: 'Auto Detect' },
    { code: 'en', name: 'English', native_name: 'English' },
    { code: 'hi', name: 'Hindi', native_name: 'हिन्दी' },
    { code: 'mr', name: 'Marathi', native_name: 'मराठी' },
    { code: 'es', name: 'Spanish', native_name: 'Español' },
    { code: 'fr', name: 'French', native_name: 'Français' },
    { code: 'de', name: 'German', native_name: 'Deutsch' },
    { code: 'ja', name: 'Japanese', native_name: '日本語' }
  ]);

  // Preload state for pipeline cross-navigation
  const [pipelineInspectText, setPipelineInspectText] = useState("I am going to college.");
  const [pipelineSrc, setPipelineSrc] = useState("en");
  const [pipelineTgt, setPipelineTgt] = useState("hi");

  useEffect(() => {
    async function loadLangs() {
      try {
        const langs = await fetchLanguages();
        if (langs && langs.length > 0) {
          setLanguages(langs);
        }
      } catch (err) {
        console.error("Failed to load languages list from backend", err);
      }
    }
    loadLangs();
  }, []);

  const handleInspectInPipeline = (text, src, tgt) => {
    setPipelineInspectText(text);
    setPipelineSrc(src === 'auto' ? 'en' : src);
    setPipelineTgt(tgt);
    setActiveTab('pipeline');
  };

  const handleTestInStudio = (text, src, tgt) => {
    setActiveTab('studio');
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-brand-500 selection:text-white">
      
      {/* Top Navigation */}
      <Navbar 
        activeTab={activeTab} 
        setActiveTab={setActiveTab} 
        onOpenInfo={() => setIsInfoOpen(true)}
      />

      {/* Main Content Area */}
      <main className="flex-1">
        {activeTab === 'studio' && (
          <StudioView 
            languages={languages} 
            onInspectInPipeline={handleInspectInPipeline}
          />
        )}

        {activeTab === 'pipeline' && (
          <PipelineVisualizer 
            initialText={pipelineInspectText}
            initialSrc={pipelineSrc}
            initialTgt={pipelineTgt}
          />
        )}

        {activeTab === 'challenges' && (
          <ChallengesExplorer 
            onTestInStudio={handleTestInStudio}
          />
        )}

        {activeTab === 'dialogue' && (
          <DialogueAssistant 
            languages={languages}
          />
        )}

        {activeTab === 'document' && (
          <DocumentTranslator 
            languages={languages}
          />
        )}

        {activeTab === 'phrasebook' && (
          <PhrasebookView />
        )}
      </main>

      {/* Presentation Info Modal */}
      <InfoModal 
        isOpen={isInfoOpen} 
        onClose={() => setIsInfoOpen(false)} 
      />

      {/* Academic Presentation Footer */}
      <footer className="border-t border-slate-900 bg-slate-950 py-6 px-4 sm:px-6 lg:px-8 mt-12">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4 text-xs text-slate-400">
          <div className="flex items-center gap-2">
            <GraduationCap className="w-4 h-4 text-brand-400" />
            <span>
              <b>Presented by: Aryan</b> • B.Tech AI & Data Science • <b>D.Y. Patil University</b>
            </span>
          </div>
          
          <div className="text-center font-mono text-[11px] text-cyan-400/80">
            Natural Language Processing • "Language ≠ Just Words → Context + Culture + Meaning"
          </div>

          <div className="flex items-center gap-1.5 text-slate-400">
            <span>PolyGlot NLP Workbench</span>
            <span>•</span>
            <span className="text-emerald-400 font-semibold">FastAPI + React</span>
          </div>
        </div>
      </footer>

    </div>
  );
}

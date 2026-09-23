# PolyGlot NLP: Multilingual Translation Assistant

> **Subject**: Natural Language Processing  
> **Program**: B.Tech • AI & Data Science  
> **Presented by**: Aryan  
> **Institution**: D.Y. Patil University  
> *"Language ≠ Just Words → Context + Culture + Meaning"*

---

## 📖 Overview

**PolyGlot NLP** is a comprehensive, production-grade full-stack web application implementing the principles of Natural Language Processing (NLP) for multilingual communication. Designed directly around the academic presentation **"Multilingual NLP Translation Assistants: How Natural Language Processing enables communication across languages"**, this system moves beyond naive word-for-word substitution to achieve **meaning-preserving, culturally-aware, and grammatically nuanced translation**.

---

## 🌟 Key Features & Slide Mapping

| Slide | Academic Concept | Implemented Feature in PolyGlot NLP |
|---|---|---|
| **Slide 2** | *What is Multilingual NLP?* | End-to-end multi-modal pipeline (Text, Speech, Documents) preserving meaning across 50+ languages. |
| **Slide 3** | *What is a Translation Assistant?* | Automatic language/script detection, phonetic transliteration, grammar assistance, and real-time dialogue. |
| **Slide 4** | *6-Step NLP Pipeline* | Interactive visual inspector showing: Input → Detect → Encode → Translate → Decode → Output. |
| **Slide 5** | *Core NLP Technologies* | Subword Tokenization (BPE), Embeddings, Self-Attention, Transformers, and NMT. |
| **Slide 6** | *Transformer Architecture* | Visual Encoder-Decoder workflow with an **interactive Multi-Head Cross-Attention Heatmap** (e.g. *"I am going to college"* ⇄ *"मैं कॉलेज जा रहा हूँ"*). |
| **Slide 7** | *6 Major Challenges* | Dedicated **Challenges Explorer** demonstrating: **Ambiguity**, **Context**, **Idioms & Slang**, **Low-Resource**, **Culture**, and **Code-Switching (Hinglish)**. |
| **Slide 8** | *Applications* | Document localization (.md, .json, .csv, .txt), education flashcards, healthcare/tourism terminology glossaries. |
| **Slide 9** | *AI Assistant Benchmark* | Real-time translation of *"मुझे कल कॉलेज जाना है।"* → *"I have to go to college tomorrow."* with TTS, STT, and Transliteration. |
| **Slide 10** | *Future Directions* | Semantic fidelity scoring (Back-translation drift verification) & bidirectional conversational dialogue. |

---

## 🛠️ Architecture & Tech Stack

- **Frontend**:
  - React 18 with Vite
  - Tailwind CSS + Glassmorphism design system
  - Lucide Icons
  - Web Speech API (Speech Recognition STT + Speech Synthesis TTS)
  - Interactive Multi-Head Attention Heatmap & Stepper
- **Backend**:
  - Python 3.12 + FastAPI
  - Deep-Translator (Google NMT, MyMemory, Offline benchmark corpus)
  - Language & Script Identification (`langdetect` + Unicode regex)
  - Transliteration Engine (Devanagari ⇄ Romanized Latin phonetics)
  - SQLite persistent storage for phrasebook & translation history
  - Document parser & localized reassembly engine (.txt, .md, .json, .csv)

---

## 🚀 Quick Start Guide

### 1. Launch Everything in One Click (Windows)
Double-click:
```bash
run_project.bat
```

### 2. Or Run Individually:

#### Backend:
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --port 8000 --reload
```
API Documentation will be live at: `http://localhost:8000/docs`

#### Frontend:
```bash
cd frontend
npm install
npm run dev
```
Web Application will be live at: `http://localhost:5173`

---

## 🧪 Automated Tests
Run backend test suite:
```bash
cd backend
.\venv\Scripts\python.exe -m pytest
```
All 9 test suites verify:
- Health check & API info
- Supported languages dictionary
- Script & language detection
- Slide 9 benchmark Hindi-to-English translation
- Transliteration engine
- 6-step Transformer pipeline inspection & attention matrix
- 6 Linguistic challenge scenarios
- SQLite phrasebook persistence

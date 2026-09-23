# BhashaAI (भाषाAI) — Multilingual Neural Machine Translation Engine

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![PyTorch](https://img.shields.io/badge/PyTorch-CUDA%20Accelerated-orange)
![Transformers](https://img.shields.io/badge/HuggingFace-NLLB--200-yellow)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)
![SacreBLEU](https://img.shields.io/badge/Evaluation-BLEU%20%2F%20chrF-green)

**BhashaAI** is a high-performance, GPU-accelerated multilingual machine translation platform designed specifically for **Indian Languages (Indic)** alongside major world languages. Powered by Meta's **NLLB-200** (`facebook/nllb-200-distilled-600M`) and built with **Streamlit**, BhashaAI provides instant text translation, document translation, automatic language detection, metric evaluation (BLEU/chrF), linguistic error analysis, and human evaluation tracking.

---

## 🌟 Key Features

1. **Multilingual Translation Engine**: Supports 15 high-priority languages (Hindi, Marathi, Bengali, Gujarati, Tamil, Telugu, Kannada, Malayalam, Punjabi, Odia, Urdu, English, French, German, Spanish) mapped to 200+ NLLB language codes.
2. **GPU Acceleration (CUDA)**: Automatic CUDA device detection with CPU fallback; leverages batching and FP16/FP32 precision for fast inference.
3. **Auto Language Detection**: Real-time language identification using **Lingua**.
4. **Document Translation**: Full-document text extraction and batch translation for `.txt`, `.pdf`, and `.docx` files with real-time progress indicators.
5. **Evaluation Dashboard**: Compute **BLEU** and **chrF** metrics using **SacreBLEU**, export CSV benchmarks, and visualize score comparisons & latency graphs.
6. **Error Analysis Framework**: Categorize translation errors into 10 linguistic types (morphological, syntactic, semantic, named entity, word order, omission, addition, idiom, long-context, code-mixed) with severity ratings.
7. **Human Evaluation Portal**: Standardized interface for human annotators to rate Fluency, Adequacy, Meaning Preservation, and Grammar on 1–5 scale.
8. **Translation History**: Auto-saves session translations with quick copy, download, search, and export options.

---

## 🏗️ Architecture & Project Structure

```text
d:\NLP-Capstone-main\
├── app.py                          # Streamlit application entry point
├── requirements.txt                # Dependency list
├── run_project.bat                 # One-click Windows launcher
├── README.md                       # Project documentation
│
├── src/                            # Core engine components
│   ├── config.py                   # Centralized configuration & NLLB mapping
│   ├── translator.py               # NLLB-200 loading, caching & GPU inference
│   ├── detector.py                 # Lingua auto language detection
│   ├── text_processor.py           # Text normalization & sentence segmentation
│   ├── document_processor.py        # TXT/PDF/DOCX extraction & segment translation
│   ├── evaluator.py                # SacreBLEU evaluation & graph generation
│   ├── history.py                  # JSON history management
│   └── utils.py                    # Timer context & formatting helpers
│
├── pages/                          # Multi-page Streamlit application
│   ├── 1_📝_Translate.py           # Main interactive text translation
│   ├── 2_📄_Document_Translation.py # File document translation
│   ├── 3_📊_Evaluation.py          # SacreBLEU metrics & graph visualization
│   ├── 4_🔍_Error_Analysis.py      # Linguistic error categorization
│   ├── 5_👤_Human_Evaluation.py    # 1-5 human quality rating portal
│   └── 6_📜_History.py             # Translation history browser
│
├── evaluation/                     # Standalone CLI evaluation
│   ├── evaluate.py                 # Command line evaluation script
│   └── metrics.py                  # SacreBLEU wrappers
│
├── data/
│   └── evaluation/                 # Benchmark parallel corpora (EN-HI, EN-MR, etc.)
│
├── results/                        # Saved evaluation metrics, graphs, error logs
│   ├── metrics/
│   ├── graphs/
│   ├── error_analysis/
│   └── human_evaluation/
│
└── tests/                          # PyTest / Unittest suite
    ├── test_imports.py
    ├── test_cuda.py
    ├── test_translator.py
    ├── test_detector.py
    ├── test_text_processor.py
    ├── test_evaluator.py
    └── test_history.py
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10+ (Python 3.12 recommended)
- NVIDIA GPU with CUDA support (Optional, highly recommended e.g., RTX 3060/4060/5060 or better)

### 2. Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/your-org/BhashaAI.git
cd BhashaAI
pip install -r requirements.txt
```

### 3. Running the App
Run via Streamlit CLI:
```bash
streamlit run app.py
```
Or on Windows, double-click or run:
```cmd
run_project.bat
```

---

## 🧪 Running Unit Tests

Run the complete test suite:
```bash
python -m unittest discover -s tests -p "test_*.py"
```

Or individual test modules:
```bash
python -m unittest tests/test_imports.py
python -m unittest tests/test_cuda.py
python -m unittest tests/test_text_processor.py
python -m unittest tests/test_detector.py
python -m unittest tests/test_evaluator.py
python -m unittest tests/test_history.py
```

---

## 📊 Evaluation & Benchmarking

### CLI Batch Evaluation
Run benchmark evaluation on parallel datasets without UI:
```bash
python evaluation/evaluate.py --pairs en_hi en_mr en_bn --dataset-dir data/evaluation/
```

Outputs will be saved directly to `results/metrics/` and `results/graphs/`.

---

## 🛡️ Supported Languages

| Language Name | Native Name | Code | NLLB Code | Region / Family |
|---|---|---|---|---|
| English | English | `en` | `eng_Latn` | Germanic |
| Hindi | हिन्दी | `hi` | `hin_Deva` | Indo-Aryan |
| Marathi | मराठी | `mr` | `mar_Deva` | Indo-Aryan |
| Bengali | বাংলা | `bn` | `ben_Beng` | Indo-Aryan |
| Gujarati | ગુજરાતી | `gu` | `guj_Gujr` | Indo-Aryan |
| Tamil | தமிழ் | `ta` | `tam_Taml` | Dravidian |
| Telugu | తెలుగు | `te` | `tel_Telu` | Dravidian |
| Kannada | ಕನ್ನಡ | `kn` | `kan_Knda` | Dravidian |
| Malayalam | മലയാളം | `ml` | `mal_Mlym` | Dravidian |
| Punjabi | ਪੰਜਾਬੀ | `pa` | `pan_Guru` | Indo-Aryan |
| Odia | ଓଡ଼ିଆ | `or` | `ory_Orya` | Indo-Aryan |
| Urdu | اردو | `ur` | `urd_Arab` | Indo-Aryan |
| French | Français | `fr` | `fra_Latn` | Romance |
| German | Deutsch | `de` | `deu_Latn` | Germanic |
| Spanish | Español | `es` | `spa_Latn` | Romance |

---

## 📄 License
This project is licensed under the MIT License.

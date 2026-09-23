"""
BhashaAI — Centralized Configuration
All supported languages, NLLB codes, model settings, and paths.
"""

import os
import torch
from pathlib import Path

# ── Project Paths ──────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
EVALUATION_DIR = DATA_DIR / "evaluation"
DOMAIN_DIR = DATA_DIR / "domain"
RESULTS_DIR = PROJECT_ROOT / "results"
METRICS_DIR = RESULTS_DIR / "metrics"
GRAPHS_DIR = RESULTS_DIR / "graphs"
ERROR_ANALYSIS_DIR = RESULTS_DIR / "error_analysis"
HUMAN_EVAL_DIR = RESULTS_DIR / "human_evaluation"
HISTORY_FILE = DATA_DIR / "history.json"

# Ensure directories exist
for d in [DATA_DIR, EVALUATION_DIR, DOMAIN_DIR, RESULTS_DIR,
          METRICS_DIR, GRAPHS_DIR, ERROR_ANALYSIS_DIR, HUMAN_EVAL_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ── PyTorch Performance Tuning ─────────────────────────────────
if not torch.cuda.is_available():
    import os
    num_threads = max(1, min(8, os.cpu_count() or 4))
    torch.set_num_threads(num_threads)

# ── Translation Engine Options ─────────────────────────────────
ENGINE_ONLINE = "Online (Zero-Download Instant API)"
ENGINE_LOCAL = "Local (Meta NLLB-200 Offline)"
ENGINE_OPTIONS = [ENGINE_ONLINE, ENGINE_LOCAL]

# Maps display name → MyMemory language string
MYMEMORY_LANG_MAP = {
    "English": "english",
    "Hindi": "hindi",
    "Marathi": "marathi",
    "Bengali": "bengali",
    "Gujarati": "gujarati",
    "French": "french",
    "German": "german",
    "Spanish": "spanish",
    "Italian": "italian",
    "Portuguese": "portuguese",
    "Russian": "russian",
    "Arabic": "arabic",
    "Chinese": "chinese simplified",
    "Japanese": "japanese",
    "Korean": "korean",
    "Punjabi": "punjabi",
    "Odia": "odia",
    "Tamil": "tamil india",
    "Telugu": "telugu",
    "Kannada": "kannada",
    "Malayalam": "malayalam",
    "Urdu": "urdu",
}

# ── Model Configuration ───────────────────────────────────────
MODEL_NAME = "facebook/nllb-200-distilled-600M"

# ── Device Selection ───────────────────────────────────────────
def get_device():
    """Select the best available device: CUDA GPU > CPU."""
    if torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")

def get_device_info():
    """Return a dict with device information for display."""
    device = get_device()
    info = {
        "device": str(device),
        "cuda_available": torch.cuda.is_available(),
        "gpu_name": None,
        "gpu_memory_total": None,
        "gpu_memory_allocated": None,
        "torch_version": torch.__version__,
        "cuda_version": torch.version.cuda if torch.cuda.is_available() else None,
    }
    if torch.cuda.is_available():
        info["gpu_name"] = torch.cuda.get_device_name(0)
        info["gpu_memory_total"] = f"{torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB"
        info["gpu_memory_allocated"] = f"{torch.cuda.memory_allocated(0) / 1e6:.1f} MB"
    return info

# ── Translation Parameters ────────────────────────────────────
MAX_INPUT_LENGTH = 512       # Max tokens per segment for NLLB
BEAM_SIZE = 1                # Greedy decoding (1 = fastest sub-second inference)
MAX_NEW_TOKENS = 256         # Max generated tokens per segment
SENTENCE_SPLIT_THRESHOLD = 200  # Characters before splitting into sentences

# ── Supported Languages ───────────────────────────────────────
# Maps display name → NLLB code
# The NLLB model uses BCP-47-like codes with script suffixes.
SUPPORTED_LANGUAGES = {
    "English":    "eng_Latn",
    "Hindi":      "hin_Deva",
    "Marathi":    "mar_Deva",
    "Bengali":    "ben_Beng",
    "Gujarati":   "guj_Gujr",
    "French":     "fra_Latn",
    "German":     "deu_Latn",
    "Spanish":    "spa_Latn",
    "Italian":    "ita_Latn",
    "Portuguese": "por_Latn",
    "Russian":    "rus_Cyrl",
    "Arabic":     "arb_Arab",
    "Chinese":    "zho_Hans",
    "Japanese":   "jpn_Jpan",
    "Korean":     "kor_Hang",
}

# Reverse map: NLLB code → display name
NLLB_TO_DISPLAY = {v: k for k, v in SUPPORTED_LANGUAGES.items()}

# Primary (Indian) languages for emphasis in the UI
PRIMARY_LANGUAGES = ["English", "Hindi", "Marathi", "Bengali", "Gujarati"]

# All language display names as a list (for dropdown menus)
LANGUAGE_NAMES = list(SUPPORTED_LANGUAGES.keys())

# ── Lingua → NLLB Mapping ─────────────────────────────────────
# lingua-language-detector uses its own language enum names.
# We map them to our NLLB codes.
LINGUA_TO_NLLB = {
    "ENGLISH":    "eng_Latn",
    "HINDI":      "hin_Deva",
    "MARATHI":    "mar_Deva",
    "BENGALI":    "ben_Beng",
    "GUJARATI":   "guj_Gujr",
    "FRENCH":     "fra_Latn",
    "GERMAN":     "deu_Latn",
    "SPANISH":    "spa_Latn",
    "ITALIAN":    "ita_Latn",
    "PORTUGUESE": "por_Latn",
    "RUSSIAN":    "rus_Cyrl",
    "ARABIC":     "arb_Arab",
    "CHINESE":    "zho_Hans",
    "JAPANESE":   "jpn_Jpan",
    "KOREAN":     "kor_Hang",
}

# ── Evaluation Pairs ──────────────────────────────────────────
DEFAULT_EVAL_PAIRS = [
    ("English", "Hindi"),
    ("English", "Marathi"),
    ("English", "Bengali"),
    ("English", "Gujarati"),
    ("Hindi", "English"),
    ("Marathi", "English"),
    ("English", "French"),
    ("English", "German"),
    ("English", "Spanish"),
]

# ── Error Analysis Categories ─────────────────────────────────
ERROR_CATEGORIES = [
    "Morphological",
    "Syntactic",
    "Semantic",
    "Named Entity",
    "Word Order",
    "Omission",
    "Addition",
    "Idiom",
    "Long Context",
    "Code-Mixed",
]

ERROR_SEVERITY_LEVELS = ["Low", "Medium", "High"]

# ── Human Evaluation Criteria ─────────────────────────────────
HUMAN_EVAL_CRITERIA = [
    {"name": "Fluency", "description": "How natural and fluent the translation reads", "scale": (1, 5)},
    {"name": "Adequacy", "description": "How much of the meaning is preserved", "scale": (1, 5)},
    {"name": "Meaning Preservation", "description": "Whether the core message is intact", "scale": (1, 5)},
    {"name": "Grammar", "description": "Grammatical correctness of the translation", "scale": (1, 5)},
]

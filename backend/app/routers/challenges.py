from fastapi import APIRouter
from typing import List, Dict, Any
from pydantic import BaseModel

router = APIRouter(prefix="/challenges", tags=["Linguistic Challenges"])

class ChallengeCase(BaseModel):
    id: str
    title: str
    category: str
    description: str
    example_input: str
    source_lang: str
    target_lang: str
    literal_translation: str
    contextual_nlp_translation: str
    explanation: str
    solution_mechanism: str

CHALLENGES_DATA: List[Dict[str, Any]] = [
    {
        "id": "ambiguity",
        "title": "Word Sense Ambiguity",
        "category": "AMBIGUITY",
        "description": "Words can have multiple meanings depending on syntactic category and semantic domain.",
        "example_input": "I deposited my check near the river bank.",
        "source_lang": "en",
        "target_lang": "hi",
        "literal_translation": "मैंने नदी के किनारे (River Bank) के पास अपना चेक जमा किया। (Contextual) vs नदी का किनारा (Bank of river)",
        "contextual_nlp_translation": "मैंने नदी के किनारे के पास स्थित बैंक (Financial Bank) में अपना चेक जमा किया।",
        "explanation": "The polysemous word 'bank' refers to both a financial institution and the side of a river. Transformer self-attention attends to 'check' and 'deposited' to resolve the financial sense.",
        "solution_mechanism": "Multi-Head Self-Attention embeddings assign contextual vectors based on neighboring tokens rather than static dictionary lookups."
    },
    {
        "id": "context",
        "title": "Temporal & Pragmatic Context",
        "category": "CONTEXT",
        "description": "Meaning heavily depends on surrounding verbal aspects, tense markers, and implied subjects.",
        "example_input": "मुझे कल कॉलेज जाना है।",
        "source_lang": "hi",
        "target_lang": "en",
        "literal_translation": "Me tomorrow/yesterday college to-go is.",
        "contextual_nlp_translation": "I have to go to college tomorrow.",
        "explanation": "In Hindi, the word 'कल' (kal) can represent both 'yesterday' and 'tomorrow'. The NMT model looks at the future obligation marker 'जाना है' to infer tomorrow rather than yesterday.",
        "solution_mechanism": "Bidirectional contextual encoders (BERT/mBART) analyze past and future tokens simultaneously to resolve temporal orientation."
    },
    {
        "id": "idioms",
        "title": "Idiomatic Expressions & Figurative Language",
        "category": "IDIOMS & SLANG",
        "description": "Literal word-for-word translation may be completely erroneous or comical.",
        "example_input": "It is raining cats and dogs outside.",
        "source_lang": "en",
        "target_lang": "hi",
        "literal_translation": "बाहर बिल्लियों और कुत्तों की बारिश हो रही है। (Literal error)",
        "contextual_nlp_translation": "बाहर मूसलाधार बारिश हो रही है। (Preserved figurative meaning)",
        "explanation": "A naive dictionary substitutes 'cats' and 'dogs', creating an absurd sentence. Multilingual NLP maps the figurative idiom to the native Hindi equivalent 'मूसलाधार बारिश'.",
        "solution_mechanism": "Phrase-level phrasebook embeddings and large-scale parallel bilingual corpora training."
    },
    {
        "id": "low_resource",
        "title": "Low-Resource & Regional Languages",
        "category": "LOW-RESOURCE",
        "description": "Many world languages and regional Indian dialects suffer from limited parallel corpora and sparse digital text.",
        "example_input": "तुम्ही उद्या येणार का?",
        "source_lang": "mr",
        "target_lang": "en",
        "literal_translation": "You tomorrow come will?",
        "contextual_nlp_translation": "Will you come tomorrow?",
        "explanation": "Marathi and other regional languages have fewer web corpora than English. Modern NLP overcomes this via cross-lingual transfer learning (e.g. leveraging shared Hindi/Sanskrit roots).",
        "solution_mechanism": "Cross-lingual Zero-Shot Transfer & Multilingual Pretrained Models (like IndicTrans2, mBART, NLLB-200)."
    },
    {
        "id": "culture",
        "title": "Cultural Nuance & Honorific Registers",
        "category": "CULTURE",
        "description": "Certain expressions have socio-cultural hierarchy with no 1:1 English mapping.",
        "example_input": "आप बैठिए vs तुम बैठो vs तू बैठ",
        "source_lang": "hi",
        "target_lang": "en",
        "literal_translation": "All three translate to English simply as 'You sit'.",
        "contextual_nlp_translation": "आप बैठिए -> 'Please have a seat (Formal/Respectful)' | तुम बैठो -> 'Take a seat (Familiar)' | तू बैठ -> 'Sit down (Intimate/Casual)'",
        "explanation": "English has a single pronoun 'you', obscuring the distinction between high honorific (आप), peer equality (तुम), and intimate/crude (तू). The assistant provides tone metadata.",
        "solution_mechanism": "Linguistic Assistance layer tagging pragmatic register, politeness markers, and socio-cultural annotations."
    },
    {
        "id": "code_switching",
        "title": "Code-Switching & Hybrid Dialects (Hinglish)",
        "category": "CODE-SWITCHING",
        "description": "Bilingual speakers spontaneously alternate between languages in a single utterance.",
        "example_input": "Mujhe kal college jaana hai because exam conduct ho raha hai.",
        "source_lang": "hi",
        "target_lang": "en",
        "literal_translation": "Mixed Hindi in Roman script mixed with English vocabulary.",
        "contextual_nlp_translation": "I have to go to college tomorrow because the exam is being conducted.",
        "explanation": "Code-switching violates single-script and single-language assumptions. The assistant identifies phonetic Hindi words written in English, normalizes them, and produces coherent translation.",
        "solution_mechanism": "Hybrid script tokenization, language-identification per token, and transliteration normalization."
    }
]

@router.get("/", response_model=List[ChallengeCase])
def get_challenges():
    """Returns the 6 major NLP translation challenges and their solutions."""
    return CHALLENGES_DATA

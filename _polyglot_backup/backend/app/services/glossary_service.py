"""
Glossary Service
Maintains domain-specific terminologies (Tech, Medical, Legal, Business, Tourism)
Ensures critical domain terminology is preserved and accurately translated without generic drift.
"""
from typing import Dict, Optional
import re

DOMAIN_GLOSSARIES: Dict[str, Dict[str, Dict[str, str]]] = {
    "tech": {
        # Source (en) -> Target (hi, es, fr, de, etc.)
        "artificial intelligence": {
            "hi": "कृत्रिम बुद्धिमत्ता (Artificial Intelligence)",
            "es": "inteligencia artificial",
            "fr": "intelligence artificielle",
            "de": "künstliche Intelligenz"
        },
        "machine learning": {
            "hi": "मशीन लर्निंग (Machine Learning)",
            "es": "aprendizaje automático",
            "fr": "apprentissage automatique",
            "de": "maschinelles Lernen"
        },
        "natural language processing": {
            "hi": "प्राकृतिक भाषा प्रसंस्करण (NLP)",
            "es": "procesamiento del lenguaje natural",
            "fr": "traitement du langage naturel",
            "de": "Verarbeitung natürlicher Sprache"
        },
        "database": {
            "hi": "डेटाबेस (Database)",
            "es": "base de datos",
            "fr": "base de données",
            "de": "Datenbank"
        },
        "neural network": {
            "hi": "तंत्रिका नेटवर्क (Neural Network)",
            "es": "red neuronal",
            "fr": "réseau neuronal",
            "de": "neuronales Netz"
        },
        "deployment": {
            "hi": "परिनियोजन (Deployment)",
            "es": "despliegue",
            "fr": "déploiement",
            "de": "Bereitstellung"
        }
    },
    "medical": {
        "hypertension": {
            "hi": "उच्च रक्तचाप (Hypertension)",
            "es": "hipertensión arterial",
            "fr": "hypertension artérielle",
            "de": "Bluthochdruck"
        },
        "prescription": {
            "hi": "दवा का पर्चा (Prescription)",
            "es": "receta médica",
            "fr": "ordonnance",
            "de": "Rezept"
        },
        "symptoms": {
            "hi": "लक्षण (Symptoms)",
            "es": "síntomas",
            "fr": "symptômes",
            "de": "Symptome"
        },
        "dosage": {
            "hi": "खुराक (Dosage)",
            "es": "dosis",
            "fr": "posologie",
            "de": "Dosierung"
        }
    },
    "legal": {
        "contract": {
            "hi": "अनुबंध / संविदा (Contract)",
            "es": "contrato",
            "fr": "contrat",
            "de": "Vertrag"
        },
        "liability": {
            "hi": "देयता / उत्तरदायित्व (Liability)",
            "es": "responsabilidad legal",
            "fr": "responsabilité",
            "de": "Haftung"
        },
        "intellectual property": {
            "hi": "बौद्धिक संपदा (Intellectual Property)",
            "es": "propiedad intelectual",
            "fr": "propriété intellectuelle",
            "de": "geistiges Eigentum"
        }
    },
    "business": {
        "revenue": {
            "hi": "राजस्व / आय (Revenue)",
            "es": "ingresos",
            "fr": "chiffre d'affaires",
            "de": "Umsatz"
        },
        "stakeholder": {
            "hi": "हितधारक (Stakeholder)",
            "es": "parte interesada",
            "fr": "partie prenante",
            "de": "Interessengruppe"
        },
        "quarterly report": {
            "hi": "त्रैमासिक रिपोर्ट (Quarterly Report)",
            "es": "informe trimestral",
            "fr": "rapport trimestriel",
            "de": "Quartalsbericht"
        }
    },
    "tourism": {
        "boarding pass": {
            "hi": "बोर्डिंग पास (Boarding Pass)",
            "es": "tarjeta de embarque",
            "fr": "carte d'embarquement",
            "de": "Bordkarte"
        },
        "sightseeing": {
            "hi": "पर्यटन / दर्शनीय स्थल (Sightseeing)",
            "es": "visitas turísticas",
            "fr": "visite touristique",
            "de": "Besichtigung"
        }
    }
}

class GlossaryService:
    def __init__(self):
        self.glossaries = DOMAIN_GLOSSARIES

    def apply_glossary(self, text: str, domain: str, target_lang: str) -> str:
        """Substitutes domain terms with accurate domain target phrases."""
        if not domain or domain == "general" or domain not in self.glossaries:
            return text

        domain_terms = self.glossaries[domain]
        result = text

        for term, translations in domain_terms.items():
            if target_lang in translations:
                target_term = translations[target_lang]
                # Case-insensitive term search with word boundaries
                pattern = re.compile(rf'\b{re.escape(term)}\b', re.IGNORECASE)
                result = pattern.sub(target_term, result)

        return result

    def get_supported_domains(self):
        return list(self.glossaries.keys()) + ["general"]

glossary_service = GlossaryService()

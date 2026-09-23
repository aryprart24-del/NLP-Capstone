from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import translate, pipeline, challenges, dialogue, documents, history

app = FastAPI(
    title="Multilingual NLP Translation Assistant API",
    description="Full-stack AI/NLP-powered translation and linguistic assistant workbench for Aryan's D.Y. Patil University B.Tech AI & Data Science presentation.",
    version="1.0.0"
)

# CORS configuration for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(translate.router, prefix="/api")
app.include_router(pipeline.router, prefix="/api")
app.include_router(challenges.router, prefix="/api")
app.include_router(dialogue.router, prefix="/api")
app.include_router(documents.router, prefix="/api")
app.include_router(history.router, prefix="/api")

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Multilingual NLP Translation Assistant",
        "version": "1.0.0"
    }

@app.get("/api/info")
def project_info():
    return {
        "project": "Multilingual NLP Translation Assistants",
        "subtitle": "How Natural Language Processing enables communication across languages",
        "presented_by": "Aryan",
        "degree": "B.Tech • AI & Data Science",
        "institution": "D.Y. Patil University",
        "features": [
            "Zero-Config Multi-Engine NMT Translation",
            "Subword Tokenization (BPE) & Attention Weight Inspection",
            "Phonetic Transliteration (Devanagari <-> Latin/Roman)",
            "Semantic Back-Translation & Drift Scoring",
            "Real-Time Two-Way Bilingual Dialogue Mode",
            "Preserving Structure Document Translation (.md, .json, .csv, .txt)",
            "The 6 NLP Challenges Explorer (Ambiguity, Context, Idioms, Low-Resource, Culture, Code-Switching)"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

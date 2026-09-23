import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_info():
    response = client.get("/api/info")
    assert response.status_code == 200
    data = response.json()
    assert data["presented_by"] == "Aryan"
    assert "D.Y. Patil University" in data["institution"]

def test_languages_list():
    response = client.get("/api/translate/languages")
    assert response.status_code == 200
    langs = response.json()
    codes = [l["code"] for l in langs]
    assert "en" in codes
    assert "hi" in codes
    assert "mr" in codes
    assert "es" in codes

def test_language_detection_devanagari():
    response = client.post("/api/translate/detect", json={"text": "मुझे कल कॉलेज जाना है।"})
    assert response.status_code == 200
    data = response.json()
    assert data["detected_code"] == "hi"
    assert data["script"] == "Devanagari"

def test_translation_benchmark_slide_example():
    # Aryan's Slide 9 Example
    response = client.post("/api/translate/", json={
        "text": "मुझे कल कॉलेज जाना है।",
        "source_lang": "hi",
        "target_lang": "en",
        "include_back_translation": True
    })
    assert response.status_code == 200
    data = response.json()
    assert "college" in data["translated_text"].lower()
    assert data["fidelity_score"] is not None

def test_transliteration():
    # Aryan's Slide 6 Transformer Example
    response = client.post("/api/translate/", json={
        "text": "I am going to college.",
        "source_lang": "en",
        "target_lang": "hi"
    })
    assert response.status_code == 200
    data = response.json()
    assert "कॉलेज" in data["translated_text"]
    assert data["transliteration"] is not None

def test_pipeline_inspect():
    # Aryan's Slide 4 & 6 Pipeline Inspection
    response = client.post("/api/pipeline/inspect", json={
        "text": "I am going to college.",
        "source_lang": "en",
        "target_lang": "hi"
    })
    assert response.status_code == 200
    data = response.json()
    assert len(data["steps"]) == 6
    assert len(data["attention_matrix"]) > 0

def test_challenges_list():
    # Aryan's Slide 7 Challenges
    response = client.get("/api/challenges/")
    assert response.status_code == 200
    challenges = response.json()
    assert len(challenges) == 6
    categories = [c["category"] for c in challenges]
    assert "AMBIGUITY" in categories
    assert "CODE-SWITCHING" in categories
    assert "IDIOMS & SLANG" in categories

def test_phrasebook():
    response = client.get("/api/history/phrasebook")
    assert response.status_code == 200
    phrases = response.json()
    assert len(phrases) > 0

const API_BASE = '/api';

export async function fetchHealth() {
  const res = await fetch(`${API_BASE}/health`);
  return res.json();
}

export async function fetchProjectInfo() {
  const res = await fetch(`${API_BASE}/info`);
  return res.json();
}

export async function fetchLanguages() {
  const res = await fetch(`${API_BASE}/translate/languages`);
  return res.json();
}

export async function detectLanguage(text) {
  const res = await fetch(`${API_BASE}/translate/detect`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text })
  });
  return res.json();
}

export async function translateText({
  text,
  source_lang = 'auto',
  target_lang = 'en',
  tone = 'neutral',
  domain = 'general',
  include_back_translation = true,
  include_linguistic_analysis = true
}) {
  const res = await fetch(`${API_BASE}/translate/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      text,
      source_lang,
      target_lang,
      tone,
      domain,
      include_back_translation,
      include_linguistic_analysis
    })
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Translation request failed' }));
    throw new Error(err.detail || 'Translation error');
  }
  return res.json();
}

export async function inspectPipeline({ text, source_lang = 'auto', target_lang = 'hi' }) {
  const res = await fetch(`${API_BASE}/pipeline/inspect`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, source_lang, target_lang })
  });
  if (!res.ok) throw new Error('Pipeline inspection failed');
  return res.json();
}

export async function fetchChallenges() {
  const res = await fetch(`${API_BASE}/challenges/`);
  return res.json();
}

export async function sendDialogueMessage({ speaker, text, speaker_a_lang, speaker_b_lang }) {
  const res = await fetch(`${API_BASE}/dialogue/message`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ speaker, text, speaker_a_lang, speaker_b_lang })
  });
  return res.json();
}

export async function uploadDocument({ file, source_lang = 'auto', target_lang = 'hi' }) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('source_lang', source_lang);
  formData.append('target_lang', target_lang);

  const res = await fetch(`${API_BASE}/documents/upload`, {
    method: 'POST',
    body: formData
  });
  if (!res.ok) throw new Error('Document translation failed');
  return res.json();
}

export async function fetchHistory() {
  const res = await fetch(`${API_BASE}/history/`);
  return res.json();
}

export async function clearHistory() {
  const res = await fetch(`${API_BASE}/history/clear`, { method: 'DELETE' });
  return res.json();
}

export async function fetchPhrasebook(category = null) {
  const url = category ? `${API_BASE}/history/phrasebook?category=${encodeURIComponent(category)}` : `${API_BASE}/history/phrasebook`;
  const res = await fetch(url);
  return res.json();
}

export async function addPhrase({ source_text, source_lang, translated_text, target_lang, category, notes }) {
  const res = await fetch(`${API_BASE}/history/phrasebook`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ source_text, source_lang, translated_text, target_lang, category, notes })
  });
  return res.json();
}

export async function deletePhrase(id) {
  const res = await fetch(`${API_BASE}/history/phrasebook/${id}`, { method: 'DELETE' });
  return res.json();
}

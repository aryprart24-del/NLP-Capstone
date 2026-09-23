# BhashaAI — Multilingual Translation System
## Product Requirements Document (PRD), Application Stack & Technical Flow

**Project Type:** B.Tech AI & Data Science Capstone  
**Domain:** Natural Language Processing (NLP), Multilingual AI, Neural Machine Translation  
**Project Name:** BhashaAI  
**Primary Platform:** Local Windows Application  
**Development Environment:** VS Code  
**Frontend/UI:** Streamlit  
**Primary Model:** `facebook/nllb-200-distilled-600M`  
**Primary Hardware:** NVIDIA GeForce RTX 5060 Ti 16 GB  
**Academic Year:** 2026–2027  

---

# 1. Executive Summary

BhashaAI is a multilingual neural machine translation system designed to translate text between English, Indian languages, and selected international languages. The system combines automatic language detection, multilingual text processing, Transformer-based neural machine translation, long-text/document translation, quantitative evaluation, error analysis, and an interactive web interface.

The core translation engine uses Meta's pretrained NLLB-200 model. The capstone contribution is not the invention of the pretrained model, but the design and implementation of the BhashaAI system around it: multilingual workflow, language detection, GPU-accelerated inference, document handling, evaluation methodology, multilingual comparison, error analysis, and optional domain adaptation.

The project is intended to demonstrate practical application of NLP syllabus concepts including morphology, syntax, semantics, language models, multilingual NLP, and machine translation.

---

# 2. Product Vision

> Build an accessible, modular, GPU-accelerated and experimentally evaluable multilingual translation platform with a particular focus on English and Indian languages.

---

# 3. Problem Statement

India and other multilingual environments contain users who may receive educational, technical, government, business, or public information in languages they do not understand comfortably.

The project addresses this problem by creating a local multilingual translation system that can:

1. Detect or receive the source language.
2. Accept text from the user.
3. Process and segment the text.
4. Translate it using a multilingual Transformer.
5. Display the translated result.
6. Translate longer text/document content.
7. Evaluate translation quality.
8. Compare multiple language pairs.
9. Analyze translation errors.
10. Maintain a translation history.

The system is an academic prototype and is not intended to replace professional translators or provide certified translations for safety-critical use.

---

# 4. Goals

## 4.1 Primary Goals

- Support multilingual text translation.
- Support Indian languages such as Hindi, Marathi, Bengali, and Gujarati.
- Provide automatic source-language detection.
- Use GPU acceleration through CUDA when available.
- Support short and long text translation.
- Provide a clean Streamlit user interface.
- Measure translation quality with BLEU and chrF.
- Compare translation quality across language pairs.
- Provide a structured error-analysis framework.
- Provide a human-evaluation framework.
- Provide an optional domain-adaptation/fine-tuning pathway.

## 4.2 Secondary Goals

- Provide translation history.
- Provide copy/download functionality.
- Display translation time.
- Display word and character counts.
- Support TXT/PDF/DOCX document translation where practical.
- Save evaluation results as CSV.
- Generate evaluation graphs.
- Produce a reproducible academic workflow.

---

# 5. Non-Goals

The initial release will not:

- Train a multilingual translation model from scratch.
- Claim to have developed NLLB-200.
- Guarantee perfect or human-equivalent translation.
- Perform certified medical, legal, financial, or safety-critical translation.
- Build a cloud-scale translation infrastructure.
- Provide speech-to-speech translation in the first version.
- Use Google Translate as the core translation engine.
- Fabricate benchmark or human-evaluation results.

---

# 6. Target Users

## 6.1 Students

Students can translate:

- academic instructions
- notices
- study material
- project documentation

## 6.2 Teachers and Educators

Teachers can translate educational material into regional languages.

## 6.3 Researchers

Researchers can evaluate multilingual translation performance and study language-pair differences.

## 6.4 General Users

Users can translate paragraphs and short documents between supported languages.

---

# 7. Supported Languages

## Primary Languages

| Language | NLLB Code | Priority |
|---|---|---|
| English | `eng_Latn` | High |
| Hindi | `hin_Deva` | High |
| Marathi | `mar_Deva` | High |
| Bengali | `ben_Beng` | High |
| Gujarati | `guj_Gujr` | High |

## Additional Languages

| Language | NLLB Code |
|---|---|
| French | `fra_Latn` |
| German | `deu_Latn` |
| Spanish | `spa_Latn` |
| Italian | `ita_Latn` |
| Portuguese | `por_Latn` |
| Russian | `rus_Cyrl` |
| Arabic | `arb_Arab` |
| Chinese | `zho_Hans` |
| Japanese | `jpn_Jpan` |
| Korean | `kor_Hang` |

The application architecture should allow additional NLLB-supported languages to be added through configuration.

---

# 8. Core Features

## 8.1 Manual Source-Language Selection

The user can choose a source language manually.

Example:

`English -> Marathi`

---

## 8.2 Automatic Language Detection

The user can choose:

`Source Language = Auto Detect`

Workflow:

```text
Input Text
   |
   v
Language Detector
   |
   v
Detected Source Language
```

Example:

```text
Input:
भारत एक विविधता से भरा देश है।

Detected:
Hindi
```

---

## 8.3 Text Translation

User workflow:

```text
Enter text
    |
Select source language
    |
Select target language
    |
Click Translate
    |
Display output
```

The interface should show:

- source language
- target language
- translated text
- translation time
- word count
- character count

---

## 8.4 Language Swap

The user can swap source and target languages.

Example:

```text
English -> Marathi
```

becomes:

```text
Marathi -> English
```

The swap must also preserve the current input/output state safely.

---

## 8.5 Character Count

The UI should display source-text character count.

Example:

`Characters: 1,248`

---

## 8.6 Word Count

The UI should display word count.

Example:

`Words: 219`

---

## 8.7 Translation History

The system should maintain recent translations.

Example:

```text
English -> Marathi
23 Sep 2026, 11:12 PM

Hindi -> English
23 Sep 2026, 11:14 PM
```

### MVP storage

JSON

### Advanced storage

SQLite

---

## 8.8 Copy Translation

The user should be able to copy the translated output.

---

## 8.9 Download Translation

Minimum:

- `.txt`

Future:

- `.pdf`
- `.docx`

---

## 8.10 Long-Text Translation

Long input should not be blindly sent as one huge model request.

Workflow:

```text
Long Text
    |
    v
Normalize
    |
    v
Sentence Segmentation
    |
    +--> Sentence 1 --> Translation
    |
    +--> Sentence 2 --> Translation
    |
    +--> Sentence 3 --> Translation
    |
    ...
    |
    v
Recombine
    |
    v
Translated Document
```

---

## 8.11 Document Translation

Recommended first release:

- TXT

Recommended advanced release:

- PDF
- DOCX

### PDF workflow

```text
PDF
 |
 v
Text Extraction
 |
 v
Text Normalization
 |
 v
Sentence/Paragraph Segmentation
 |
 v
Language Detection
 |
 v
Translation
 |
 v
Translated Content
 |
 v
Download
```

---

# 9. Evaluation Features

Evaluation is a major part of the capstone.

The evaluation module should support:

- BLEU
- chrF
- average inference time
- total inference time
- number of evaluated samples
- multiple language pairs

Evaluation requires:

```text
Source Text
Reference Translation
Model Translation
```

Then:

```text
Source + Reference + Prediction
            |
            v
      Evaluation Engine
            |
       +----+----+
       |         |
      BLEU      chrF
       |
       +--> Inference Time
```

No evaluation score should be invented or hard-coded.

---

# 10. Multi-Language Evaluation

Initial evaluation pairs:

```text
English -> Hindi
English -> Marathi
English -> Bengali
English -> Gujarati
Hindi -> English
Marathi -> English
English -> French
English -> German
English -> Spanish
```

The implementation should be configurable so more pairs can be added without changing the evaluation engine.

---

# 11. Error Analysis

The project should support analysis of:

1. Morphological errors
2. Syntactic errors
3. Semantic errors
4. Named-entity errors
5. Word-order errors
6. Omission errors
7. Addition errors
8. Idiom errors
9. Long-context errors
10. Code-mixed text errors

Example record:

```text
Source:
The student submitted the application yesterday.

Reference:
[Human reference]

Prediction:
[Model output]

Error Category:
Word Order

Explanation:
The translated sentence does not preserve the natural ordering
of the temporal phrase.
```

---

# 12. Human Evaluation

Automatic translation metrics do not fully describe translation quality.

A human-evaluation template should include:

| Criterion | Scale |
|---|---|
| Fluency | 1–5 |
| Adequacy | 1–5 |
| Meaning Preservation | 1–5 |
| Grammar | 1–5 |

Human scores must come from actual evaluators and must not be fabricated.

---

# 13. Optional Domain Adaptation

An advanced version of the project can investigate educational-domain adaptation.

Architecture:

```text
Pretrained NLLB-200
        |
        v
Educational Parallel Corpus
        |
        v
Fine-Tuning
        |
        v
Domain-Adapted NLLB
        |
        v
Comparison
```

Potential educational content:

- college notices
- examination instructions
- scholarship guidelines
- internship instructions
- academic regulations

Experimental comparison:

| System | BLEU | chrF |
|---|---:|---:|
| Pretrained NLLB-200 | Actual Result | Actual Result |
| Fine-Tuned NLLB-200 | Actual Result | Actual Result |

---

# 14. Functional Requirements

## FR-01

System shall allow source-language selection.

## FR-02

System shall allow target-language selection.

## FR-03

System shall provide automatic language detection.

## FR-04

System shall translate using NLLB-200.

## FR-05

System shall use CUDA/GPU when available.

## FR-06

System shall handle long text through controlled segmentation.

## FR-07

System shall display translation results.

## FR-08

System shall allow copy/download.

## FR-09

System shall maintain translation history.

## FR-10

System shall calculate BLEU.

## FR-11

System shall calculate chrF.

## FR-12

System shall measure inference time.

## FR-13

System shall support multiple language pairs.

## FR-14

System shall support error-analysis records.

## FR-15

System shall provide a human-evaluation template.

---

# 15. Non-Functional Requirements

## Performance

- Use GPU when available.
- Load the model once per application session.
- Avoid unnecessary model reloads.
- Provide progress indicators for long translations.

## Reliability

- Handle empty input.
- Handle invalid language selections.
- Handle language-detection failures.
- Handle large input safely.
- Display meaningful error messages.

## Usability

- Simple language selectors.
- Clear input/output areas.
- Visible translation status.
- Easy copy/download functionality.

## Maintainability

- Modular source code.
- Centralized configuration.
- Independent evaluation module.
- Clear project structure.
- Automated tests.

## Security

- Never commit API keys.
- Do not hard-code credentials.
- Do not upload private documents externally without user consent.
- Keep local project data local unless an external service is explicitly introduced.

---

# 16. Application Stack

## 16.1 Frontend

### Streamlit

Responsibilities:

- user interface
- language dropdowns
- text input
- file upload
- translation output
- history
- evaluation controls
- download/copy interface

---

## 16.2 Backend

### Python

Primary programming language.

---

## 16.3 Deep Learning

### PyTorch

Responsibilities:

- model execution
- tensors
- GPU computation
- CUDA acceleration

---

## 16.4 NLP Framework

### Hugging Face Transformers

Responsibilities:

- tokenizer
- Transformer model
- sequence generation
- multilingual language codes

---

## 16.5 Translation Model

### NLLB-200

Model:

`facebook/nllb-200-distilled-600M`

Responsibilities:

- multilingual neural translation

---

## 16.6 Language Detection

### Lingua Language Detector

Responsibilities:

- automatic source-language detection

---

## 16.7 Evaluation

### SacreBLEU

Responsibilities:

- BLEU
- chrF

---

## 16.8 Data Processing

- Pandas
- NumPy

---

## 16.9 Visualization

- Matplotlib
- Seaborn

---

## 16.10 Document Processing

Recommended:

- PyMuPDF for PDF
- python-docx for DOCX

---

## 16.11 Storage

### MVP

JSON

### Advanced

SQLite

---

## 16.12 Development

- VS Code
- Python virtual environment
- PowerShell
- Git
- GitHub

---

# 17. Complete Application Stack

```text
+--------------------------------------------------+
|                     USER                         |
+-------------------------+------------------------+
                          |
                          v
+--------------------------------------------------+
|                  STREAMLIT UI                    |
|                                                  |
| Language Selection                               |
| Text Input                                       |
| File Upload                                      |
| Translate                                        |
| History                                          |
| Evaluation                                       |
+-------------------------+------------------------+
                          |
                          v
+--------------------------------------------------+
|              PYTHON APPLICATION LAYER            |
|                                                  |
| Language Detector                               |
| Text Processor                                  |
| Document Processor                              |
| Translation Service                             |
| Evaluation Service                              |
| History Service                                 |
+-------------------------+------------------------+
                          |
             +------------+------------+
             |                         |
             v                         v
+----------------------+    +----------------------+
| Lingua Language      |    | NLLB-200 Transformer |
| Detector             |    |                      |
+----------------------+    +----------+-----------+
                                       |
                                       v
                              +---------------------+
                              | PyTorch + CUDA      |
                              | RTX 5060 Ti 16 GB   |
                              +---------------------+

                    Evaluation Layer
                          |
                +---------+---------+
                |                   |
                v                   v
             BLEU/chrF           CSV
                                  |
                                  v
                              Graphs/Reports
```

---

# 18. Technical Flow

## 18.1 Application Startup

```text
Start Application
      |
      v
Load Configuration
      |
      v
Check CUDA
      |
      v
Load Tokenizer
      |
      v
Load NLLB-200
      |
      v
Move Model to GPU
      |
      v
Cache Model
      |
      v
Display UI
```

---

# 19. Translation Flow

```text
User Input
    |
    v
Validate Input
    |
    v
Determine Source Language
    |
    +---- Manual Selection
    |
    +---- Auto Detection
    |
    v
Validate Target Language
    |
    v
Normalize Text
    |
    v
Split Long Text
    |
    v
NLLB Tokenizer
    |
    v
GPU Inference
    |
    v
Target Language Token
    |
    v
Beam-Search Generation
    |
    v
Decode Output
    |
    v
Recombine Sentences
    |
    v
Display Translation
```

---

# 20. Automatic Language Detection Flow

```text
Raw User Text
      |
      v
Lingua Detector
      |
      v
Detected Language
      |
      v
Check Supported Languages
      |
      +---- Unsupported --> Error
      |
      v
Continue to Translation
```

Language detection should occur before expensive model inference.

---

# 21. NLLB Translation Flow

The translation process is conceptually:

```text
Source Text
     |
     v
Source-Language Tokenizer
     |
     v
Subword Tokens
     |
     v
Multilingual Transformer Encoder
     |
     v
Decoder
     |
     v
Forced Target Language
     |
     v
Beam Search
     |
     v
Generated Tokens
     |
     v
Target Text
```

---

# 22. Long Document Translation Flow

```text
Document
    |
    v
Extract Text
    |
    v
Normalize
    |
    v
Paragraph Split
    |
    v
Sentence Split
    |
    v
Translate Sentence Units
    |
    v
Preserve Order
    |
    v
Rebuild Document
    |
    v
Download/Display
```

---

# 23. Evaluation Flow

```text
Benchmark Dataset
       |
       +-----------------------+
       |                       |
       v                       v
Source Text              Reference Text
       |
       v
NLLB Translation
       |
       v
Prediction
       |
       +-----------------------+
                       |
                       v
              Evaluation Engine
                       |
              +--------+--------+
              |                 |
              v                 v
            BLEU              chrF
              |
              +-------> Inference Time
                       |
                       v
                    CSV Results
                       |
                       v
                     Graphs
```

---

# 24. Recommended Project Structure

```text
BhashaAI/
|
+-- app.py
+-- requirements.txt
+-- README.md
+-- .gitignore
|
+-- src/
|   +-- __init__.py
|   +-- config.py
|   +-- translator.py
|   +-- language_detector.py
|   +-- text_processor.py
|   +-- document_processor.py
|   +-- evaluator.py
|   +-- history.py
|   +-- utils.py
|
+-- evaluation/
|   +-- evaluate.py
|   +-- metrics.py
|   +-- datasets/
|
+-- data/
|   +-- evaluation/
|   |   +-- en_hi.csv
|   |   +-- en_mr.csv
|   |   +-- en_bn.csv
|   |   +-- hi_en.csv
|   |   +-- mr_en.csv
|   |
|   +-- domain/
|
+-- results/
|   +-- metrics/
|   +-- graphs/
|   +-- error_analysis/
|   +-- human_evaluation/
|
+-- tests/
|
+-- docs/
```

---

# 25. Recommended Data Schema

## Evaluation dataset

CSV:

```csv
source,reference
"Source sentence 1","Human reference translation 1"
"Source sentence 2","Human reference translation 2"
```

## Error-analysis dataset

```csv
source,reference,prediction,error_category,explanation,severity
```

## Human evaluation dataset

```csv
source,reference,prediction,fluency,adequacy,meaning_preservation,grammar,evaluator
```

Scores should only be filled by actual human evaluators.

---

# 26. Testing Strategy

The system should test:

1. Python imports.
2. CUDA availability.
3. RTX 5060 Ti detection.
4. Model loading.
5. English → Hindi.
6. English → Marathi.
7. Hindi → English.
8. Marathi → English.
9. Same-language input.
10. Empty input.
11. Invalid language.
12. Language detection.
13. Long text.
14. Document processing.
15. BLEU calculation.
16. chrF calculation.
17. Streamlit application startup.

---

# 27. Performance Requirements

Record actual measurements for:

- model loading time
- translation time
- average translation time
- total evaluation time
- GPU memory usage where practical

Never hard-code performance results.

---

# 28. Research Component

The capstone should investigate:

> How does a multilingual Transformer model perform across Indian and international language pairs, and how does domain-specific adaptation affect translation quality for educational content?

### Research Questions

#### RQ1

How does NLLB-200 perform across English-to-Indian language pairs?

#### RQ2

How does translation quality differ between Indian and European language pairs?

#### RQ3

Does educational-domain fine-tuning improve translation quality?

#### RQ4

What translation errors occur most frequently across different language pairs?

---

# 29. Experimental Design

## Experiment 1 — Multilingual Translation

```text
NLLB-200
   |
   +--> English -> Hindi
   +--> English -> Marathi
   +--> English -> Bengali
   +--> English -> Gujarati
   +--> English -> French
   +--> English -> German
   +--> English -> Spanish
```

Measure:

- BLEU
- chrF
- inference time

---

## Experiment 2 — Direction Comparison

```text
English -> Marathi
Marathi -> English

English -> Hindi
Hindi -> English
```

Compare language direction effects.

---

## Experiment 3 — Domain Adaptation

```text
Pretrained NLLB
       |
       v
Educational Parallel Corpus
       |
       v
Fine-Tuning
       |
       v
Fine-Tuned NLLB
       |
       v
Held-Out Evaluation
```

Compare:

- BLEU
- chrF
- human evaluation
- terminology accuracy

---

# 30. Evaluation Interpretation

Do not interpret BLEU or chrF as complete measures of translation quality.

For example:

```text
Higher BLEU
```

generally means stronger overlap with the reference, but a valid paraphrase can receive a lower lexical-overlap score.

Therefore the project should combine:

```text
Automatic Metrics
+
Human Evaluation
+
Error Analysis
```

---

# 31. Limitations

The report should explicitly mention:

1. Translation quality varies between language pairs.
2. Low-resource languages may have lower quality than high-resource languages.
3. Automatic metrics do not fully capture semantic quality.
4. Sentence-by-sentence translation can lose document-level context.
5. Named entities and idioms can be difficult.
6. Code-mixed text can reduce reliability.
7. A pretrained model can contain biases or limitations inherited from its training data.
8. GPU memory limits large experiments.
9. Domain-specific terminology may require adaptation.
10. Model predictions should not be treated as certified translations.

---

# 32. Future Scope

Possible future extensions:

### Speech Translation

```text
Speech
 |
v
Automatic Speech Recognition
 |
v
NLLB Translation
 |
v
Text-to-Speech
```

### OCR Translation

```text
Image
 |
v
OCR
 |
v
Language Detection
 |
v
Translation
```

### Mobile Application

Android/iOS front end connected to an inference service.

### Better Document-Level Context

Use context-aware document translation instead of independent sentence translation.

### Terminology Management

Allow users to define preferred translations for technical terms.

### Human-in-the-Loop Translation

Let users correct model output and save approved corrections.

### Domain Adaptation

Fine-tune for education, technical, government, or other domains.

---

# 33. Security and Privacy

The initial system is intended to run locally.

Recommended principle:

```text
User Document
     |
     v
Local Processing
     |
     v
Local Translation Model
     |
     v
Local Output
```

This minimizes unnecessary transfer of user documents to external services.

If cloud services are added later, privacy requirements must be revisited.

---

# 34. Acceptance Criteria

The project is considered successfully implemented when:

### Core

- [ ] Streamlit starts successfully.
- [ ] NLLB-200 loads.
- [ ] CUDA is detected.
- [ ] RTX 5060 Ti is used.
- [ ] English → Hindi works.
- [ ] English → Marathi works.
- [ ] Hindi → English works.
- [ ] Marathi → English works.
- [ ] Automatic language detection works.

### UI

- [ ] Language selection works.
- [ ] Swap works.
- [ ] Clear works.
- [ ] Character count works.
- [ ] Word count works.
- [ ] Translation time is displayed.
- [ ] Translation can be copied.
- [ ] Translation can be downloaded.
- [ ] History works.

### Document

- [ ] TXT translation works.
- [ ] Long text is handled safely.
- [ ] PDF/DOCX support works if included.

### Evaluation

- [ ] BLEU works.
- [ ] chrF works.
- [ ] Inference time is recorded.
- [ ] Multiple language pairs can be evaluated.
- [ ] Results are saved to CSV.
- [ ] Graphs are generated.

### Academic

- [ ] Error-analysis framework is available.
- [ ] Human-evaluation template exists.
- [ ] No fabricated experimental results.
- [ ] Limitations are documented.
- [ ] References are included.

---

# 35. Development Roadmap

## Phase 1 — Environment

- Python
- Virtual environment
- CUDA PyTorch
- Dependencies

## Phase 2 — Core Translation

- NLLB model
- tokenizer
- GPU inference
- translation function

## Phase 3 — Language Detection

- Lingua
- supported-language validation
- auto detection

## Phase 4 — Application UI

- Streamlit
- translation controls
- results
- history

## Phase 5 — Documents

- TXT
- PDF
- DOCX

## Phase 6 — Evaluation

- benchmark dataset
- BLEU
- chrF
- timing
- graphs

## Phase 7 — Error Analysis

- linguistic categories
- saved examples
- manual analysis

## Phase 8 — Domain Adaptation

- educational corpus
- fine-tuning
- comparison

## Phase 9 — Finalization

- testing
- README
- report
- PPT
- demo
- viva preparation

---

# 36. Capstone Deliverables

Final project should contain:

```text
1. Source Code
2. Streamlit Application
3. Requirements File
4. Evaluation Dataset
5. Evaluation Scripts
6. Evaluation Results
7. Graphs
8. Error Analysis
9. Human Evaluation Template
10. Project Report
11. Presentation
12. README
13. Test Suite
14. Demo
```

---

# 37. Final System Architecture

```text
                         USER
                           |
                           v
                  +------------------+
                  |   STREAMLIT UI   |
                  +--------+---------+
                           |
                           v
                +---------------------+
                | Input Validation    |
                +----------+----------+
                           |
                           v
                +---------------------+
                | Language Detection  |
                | or Manual Selection |
                +----------+----------+
                           |
                           v
                +---------------------+
                | Text Processing     |
                | Normalization       |
                | Segmentation        |
                +----------+----------+
                           |
                           v
                +---------------------+
                | NLLB Tokenizer      |
                +----------+----------+
                           |
                           v
                +---------------------+
                | NLLB-200 Transformer|
                +----------+----------+
                           |
                           v
                +---------------------+
                | PyTorch + CUDA      |
                | RTX 5060 Ti 16 GB   |
                +----------+----------+
                           |
                           v
                +---------------------+
                | Target Text         |
                | Generation          |
                +----------+----------+
                           |
                 +---------+---------+
                 |                   |
                 v                   v
          +-------------+     +-------------+
          | Translation |     | Evaluation  |
          | Output      |     | BLEU/chrF   |
          +-------------+     +-------------+
                 |                   |
                 v                   v
          +-------------+     +-------------+
          | History /   |     | CSV / Graphs|
          | Download    |     +-------------+
          +-------------+
```

---

# 38. Final Product Definition

### BhashaAI is:

> A local, GPU-accelerated multilingual neural machine translation platform that combines automatic language detection, multilingual Transformer-based translation, document processing, quantitative evaluation, human evaluation, and translation error analysis.

### It is not:

> A new translation model or a claim of perfect factual or professional translation.

The project contribution is the system, experiments, evaluation, analysis and application built around a pretrained multilingual translation model.

---

# 39. Suggested Final Project Title

## Multilingual Neural Machine Translation and Domain Adaptation for English and Indian Languages Using Transformer Models

### Application Name

# BhashaAI

### Tagline

> **Breaking Language Barriers with Multilingual AI**

